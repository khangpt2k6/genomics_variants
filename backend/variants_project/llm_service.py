"""
LLM Service for Cancer Trend Prediction and Graph Generation

This module provides AI-powered services for:
- Predicting cancer variant trends
- Generating graphs and visualizations using LLM
- Analyzing variant data patterns
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from django.conf import settings
from variants.models import Variant, ClinicalSignificance, DrugResponse

logger = logging.getLogger(__name__)


class CancerTrendPredictor:
    """AI-powered cancer trend prediction service"""

    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.1,
            model_name="gpt-4",
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )

    def predict_variant_trends(self, days_ahead: int = 30) -> Dict[str, Any]:
        """
        Predict future cancer variant trends using historical data and AI analysis

        Args:
            days_ahead: Number of days to predict ahead

        Returns:
            Dictionary containing trend predictions and insights
        """
        try:
            # Get historical variant data
            historical_data = self._get_historical_variant_data()

            if not historical_data:
                return {"error": "Insufficient historical data for prediction"}

            # Analyze trends using AI
            trend_analysis = self._analyze_trends_with_llm(historical_data)

            # Generate predictions
            predictions = self._generate_predictions(historical_data, days_ahead)

            # Create trend visualizations
            trend_charts = self._create_trend_visualizations(historical_data, predictions)

            return {
                "predictions": predictions,
                "analysis": trend_analysis,
                "charts": trend_charts,
                "confidence_score": self._calculate_confidence_score(historical_data)
            }

        except Exception as e:
            logger.error(f"Error predicting variant trends: {str(e)}")
            return {"error": str(e)}

    def _get_historical_variant_data(self) -> List[Dict]:
        """Retrieve historical variant data for trend analysis"""
        # Get variants from the last 6 months
        six_months_ago = datetime.now() - timedelta(days=180)

        variants = Variant.objects.filter(
            created_at__gte=six_months_ago
        ).select_related('clinical_significance', 'drug_responses')

        historical_data = []
        for variant in variants:
            data_point = {
                'date': variant.created_at.date().isoformat(),
                'chromosome': variant.chromosome,
                'gene': variant.gene_symbol,
                'impact': variant.impact,
                'gnomad_af': variant.gnomad_af,
                'clinical_significance': None,
                'drug_responses': []
            }

            # Add clinical significance if available
            if hasattr(variant, 'clinical_significance') and variant.clinical_significance.exists():
                clin_sig = variant.clinical_significance.first()
                data_point['clinical_significance'] = clin_sig.significance

            # Add drug responses
            drug_responses = variant.drug_responses.all()
            data_point['drug_responses'] = [
                {
                    'drug': dr.drug_name,
                    'response_type': dr.response_type,
                    'evidence_level': dr.evidence_level
                } for dr in drug_responses
            ]

            historical_data.append(data_point)

        return historical_data

    def _analyze_trends_with_llm(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """Use LLM to analyze trends in the variant data"""

        # Prepare data summary for LLM
        data_summary = self._prepare_data_summary(historical_data)

        prompt = PromptTemplate(
            input_variables=["data_summary"],
            template="""
            Analyze the following cancer variant data trends and provide insights:

            {data_summary}

            Please provide:
            1. Key trends in variant discovery over time
            2. Most significant genes showing increased variant frequency
            3. Clinical significance patterns
            4. Drug response implications
            5. Risk assessment for future trends
            6. Recommendations for monitoring

            Format your response as a JSON object with these keys:
            - key_trends
            - significant_genes
            - clinical_patterns
            - drug_implications
            - risk_assessment
            - recommendations
            """
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)
        analysis_result = chain.run(data_summary=data_summary)

        try:
            return json.loads(analysis_result)
        except json.JSONDecodeError:
            # Fallback if LLM doesn't return valid JSON
            return {
                "key_trends": ["Analysis completed but formatting issue occurred"],
                "significant_genes": [],
                "clinical_patterns": [],
                "drug_implications": [],
                "risk_assessment": "Unable to assess",
                "recommendations": ["Review data manually"]
            }

    def _prepare_data_summary(self, historical_data: List[Dict]) -> str:
        """Prepare a summary of the data for LLM analysis"""
        df = pd.DataFrame(historical_data)

        if df.empty:
            return "No data available for analysis"

        # Group by date and calculate metrics
        daily_stats = df.groupby('date').agg({
            'chromosome': 'count',
            'gene': lambda x: x.value_counts().index[0] if len(x.value_counts()) > 0 else None,
            'impact': lambda x: x.value_counts().to_dict(),
            'clinical_significance': lambda x: x.value_counts().to_dict() if x.notna().any() else {}
        }).reset_index()

        # Calculate gene frequencies
        gene_freq = df['gene'].value_counts().head(10).to_dict()

        # Impact distribution
        impact_dist = df['impact'].value_counts().to_dict()

        # Clinical significance distribution
        clin_sig_dist = df['clinical_significance'].value_counts().to_dict()

        summary = f"""
        Historical Data Summary:
        - Total variants analyzed: {len(df)}
        - Date range: {df['date'].min()} to {df['date'].max()}
        - Daily average variants: {len(df) / len(daily_stats):.1f}

        Top Genes by Frequency:
        {json.dumps(gene_freq, indent=2)}

        Impact Distribution:
        {json.dumps(impact_dist, indent=2)}

        Clinical Significance Distribution:
        {json.dumps(clin_sig_dist, indent=2)}

        Recent Trends (last 30 days):
        - Average daily variants: {len(df[df['date'] >= (datetime.now() - timedelta(days=30)).date()]) / 30:.1f}
        """

        return summary

    def _generate_predictions(self, historical_data: List[Dict], days_ahead: int) -> Dict[str, Any]:
        """Generate statistical predictions for future trends"""
        df = pd.DataFrame(historical_data)

        if df.empty or len(df) < 7:  # Need at least a week of data
            return {"error": "Insufficient data for prediction"}

        # Convert dates and sort
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')

        # Group by date to get daily counts
        daily_counts = df.groupby('date').size().reset_index(name='count')

        # Fill missing dates with 0
        date_range = pd.date_range(start=daily_counts['date'].min(),
                                 end=daily_counts['date'].max())
        daily_counts = daily_counts.set_index('date').reindex(date_range, fill_value=0).reset_index()
        daily_counts.columns = ['date', 'count']

        # Prepare data for regression
        daily_counts['days_since_start'] = (daily_counts['date'] - daily_counts['date'].min()).dt.days

        # Fit linear regression
        X = daily_counts[['days_since_start']]
        y = daily_counts['count']

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = LinearRegression()
        model.fit(X_scaled, y)

        # Generate predictions
        future_dates = pd.date_range(start=daily_counts['date'].max() + timedelta(days=1),
                                   periods=days_ahead)
        future_days = np.arange(len(daily_counts), len(daily_counts) + days_ahead).reshape(-1, 1)
        future_days_scaled = scaler.transform(future_days)

        predictions = model.predict(future_days_scaled)

        # Calculate trend direction
        slope = model.coef_[0]
        if slope > 0.1:
            trend = "increasing"
        elif slope < -0.1:
            trend = "decreasing"
        else:
            trend = "stable"

        return {
            "predicted_counts": predictions.tolist(),
            "future_dates": [d.date().isoformat() for d in future_dates],
            "trend_direction": trend,
            "confidence_interval": self._calculate_prediction_interval(predictions, daily_counts['count'].std())
        }

    def _calculate_prediction_interval(self, predictions: np.ndarray, historical_std: float) -> List[List[float]]:
        """Calculate prediction intervals"""
        # Simple approach: ± 1 standard deviation
        intervals = []
        for pred in predictions:
            intervals.append([max(0, pred - historical_std), pred + historical_std])
        return intervals

    def _create_trend_visualizations(self, historical_data: List[Dict], predictions: Dict) -> Dict[str, Any]:
        """Create visualizations for trend analysis"""
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])

        charts = {}

        # Historical trend chart
        daily_counts = df.groupby('date').size().reset_index(name='count')

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_counts['date'],
            y=daily_counts['count'],
            mode='lines+markers',
            name='Historical Data',
            line=dict(color='blue')
        ))

        # Add predictions if available
        if 'future_dates' in predictions and 'predicted_counts' in predictions:
            future_dates = pd.to_datetime(predictions['future_dates'])
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=predictions['predicted_counts'],
                mode='lines',
                name='Predictions',
                line=dict(color='red', dash='dash')
            ))

        fig.update_layout(
            title="Cancer Variant Discovery Trends",
            xaxis_title="Date",
            yaxis_title="Number of Variants",
            template="plotly_white"
        )

        charts['trend_chart'] = json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))

        # Gene frequency chart
        gene_counts = df['gene'].value_counts().head(10)
        fig2 = px.bar(
            x=gene_counts.index,
            y=gene_counts.values,
            title="Top 10 Genes by Variant Frequency",
            labels={'x': 'Gene', 'y': 'Variant Count'}
        )
        charts['gene_chart'] = json.loads(json.dumps(fig2, cls=PlotlyJSONEncoder))

        return charts

    def _calculate_confidence_score(self, historical_data: List[Dict]) -> float:
        """Calculate confidence score for predictions"""
        if len(historical_data) < 14:  # Less than 2 weeks
            return 0.3
        elif len(historical_data) < 30:  # Less than a month
            return 0.6
        elif len(historical_data) < 90:  # Less than 3 months
            return 0.8
        else:
            return 0.9


class LLMGraphGenerator:
    """AI-powered graph generation service"""

    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.2,
            model_name="gpt-4",
            openai_api_key=os.getenv('OPENAI_API_KEY')
        )

    def generate_graph_from_data(self, data: Dict[str, Any], graph_type: str = "auto") -> Dict[str, Any]:
        """
        Generate appropriate graphs for the given data using LLM analysis

        Args:
            data: Data to visualize
            graph_type: Type of graph to generate (auto, bar, line, pie, etc.)

        Returns:
            Dictionary containing graph specifications and recommendations
        """
        try:
            # Analyze data structure
            data_analysis = self._analyze_data_structure(data)

            # Determine best graph types
            if graph_type == "auto":
                recommended_graphs = self._recommend_graph_types(data_analysis)
            else:
                recommended_graphs = [graph_type]

            # Generate graphs
            graphs = {}
            for g_type in recommended_graphs:
                graphs[g_type] = self._generate_specific_graph(data, g_type, data_analysis)

            return {
                "graphs": graphs,
                "analysis": data_analysis,
                "recommendations": self._generate_visualization_recommendations(data_analysis)
            }

        except Exception as e:
            logger.error(f"Error generating graph: {str(e)}")
            return {"error": str(e)}

    def _analyze_data_structure(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the structure and characteristics of the input data"""
        analysis = {
            "data_types": {},
            "dimensions": {},
            "value_ranges": {},
            "categorical_fields": [],
            "numerical_fields": [],
            "temporal_fields": [],
            "relationships": []
        }

        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                analysis["dimensions"][key] = len(value)

                # Check first few items to determine type
                sample = value[:min(5, len(value))]

                if all(isinstance(x, (int, float)) for x in sample):
                    analysis["data_types"][key] = "numerical"
                    analysis["numerical_fields"].append(key)
                    if len(value) > 0:
                        analysis["value_ranges"][key] = {
                            "min": min(value),
                            "max": max(value),
                            "mean": sum(value) / len(value)
                        }
                elif all(isinstance(x, str) for x in sample):
                    analysis["data_types"][key] = "categorical"
                    analysis["categorical_fields"].append(key)
                elif all(isinstance(x, dict) for x in sample):
                    analysis["data_types"][key] = "complex"
                    # Analyze nested structure
                    if sample:
                        nested_keys = set()
                        for item in sample:
                            nested_keys.update(item.keys())
                        analysis["relationships"].append({
                            "field": key,
                            "nested_fields": list(nested_keys)
                        })

        return analysis

    def _recommend_graph_types(self, data_analysis: Dict[str, Any]) -> List[str]:
        """Recommend appropriate graph types based on data analysis"""

        recommendations = []

        num_numerical = len(data_analysis["numerical_fields"])
        num_categorical = len(data_analysis["categorical_fields"])

        # Time series if we have temporal data
        if data_analysis["temporal_fields"]:
            recommendations.append("line")

        # Bar charts for categorical data
        if num_categorical > 0:
            recommendations.append("bar")

        # Pie charts for categorical distributions
        if num_categorical == 1 and num_numerical >= 1:
            recommendations.append("pie")

        # Scatter plots for relationships
        if num_numerical >= 2:
            recommendations.append("scatter")

        # Heatmaps for correlations
        if num_numerical >= 3:
            recommendations.append("heatmap")

        # Default to bar if no specific recommendations
        if not recommendations:
            recommendations = ["bar"]

        return recommendations[:3]  # Limit to top 3 recommendations

    def _generate_specific_graph(self, data: Dict[str, Any], graph_type: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a specific type of graph"""

        if graph_type == "bar":
            return self._generate_bar_chart(data, analysis)
        elif graph_type == "line":
            return self._generate_line_chart(data, analysis)
        elif graph_type == "pie":
            return self._generate_pie_chart(data, analysis)
        elif graph_type == "scatter":
            return self._generate_scatter_plot(data, analysis)
        elif graph_type == "heatmap":
            return self._generate_heatmap(data, analysis)
        else:
            return self._generate_bar_chart(data, analysis)  # Default fallback

    def _generate_bar_chart(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a bar chart specification"""
        # Find categorical and numerical fields
        cat_field = analysis["categorical_fields"][0] if analysis["categorical_fields"] else None
        num_field = analysis["numerical_fields"][0] if analysis["numerical_fields"] else None

        if not cat_field or not num_field:
            return {"error": "Insufficient data for bar chart"}

        # Prepare data for Plotly
        fig = go.Figure()

        if isinstance(data[cat_field], list) and isinstance(data[num_field], list):
            fig.add_trace(go.Bar(
                x=data[cat_field],
                y=data[num_field],
                name=num_field.title()
            ))

        fig.update_layout(
            title=f"{num_field.title()} by {cat_field.title()}",
            xaxis_title=cat_field.title(),
            yaxis_title=num_field.title(),
            template="plotly_white"
        )

        return {
            "type": "bar",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": f"Bar chart showing {num_field} distribution across {cat_field} categories"
        }

    def _generate_line_chart(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a line chart specification"""
        # Look for temporal or sequential data
        x_field = None
        y_field = analysis["numerical_fields"][0] if analysis["numerical_fields"] else None

        # Try to find a temporal field
        for field in analysis["temporal_fields"]:
            if field in data:
                x_field = field
                break

        # If no temporal field, use first available field as x
        if not x_field:
            all_fields = list(data.keys())
            x_field = all_fields[0] if all_fields else None

        if not x_field or not y_field:
            return {"error": "Insufficient data for line chart"}

        fig = go.Figure()

        if isinstance(data[x_field], list) and isinstance(data[y_field], list):
            fig.add_trace(go.Scatter(
                x=data[x_field],
                y=data[y_field],
                mode='lines+markers',
                name=y_field.title()
            ))

        fig.update_layout(
            title=f"{y_field.title()} Over Time",
            xaxis_title=x_field.title(),
            yaxis_title=y_field.title(),
            template="plotly_white"
        )

        return {
            "type": "line",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": f"Line chart showing {y_field} trends over {x_field}"
        }

    def _generate_pie_chart(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a pie chart specification"""
        cat_field = analysis["categorical_fields"][0] if analysis["categorical_fields"] else None
        num_field = analysis["numerical_fields"][0] if analysis["numerical_fields"] else None

        if not cat_field or not num_field:
            return {"error": "Insufficient data for pie chart"}

        fig = go.Figure()

        if isinstance(data[cat_field], list) and isinstance(data[num_field], list):
            fig.add_trace(go.Pie(
                labels=data[cat_field],
                values=data[num_field],
                title=num_field.title()
            ))

        fig.update_layout(
            title=f"{num_field.title()} Distribution",
            template="plotly_white"
        )

        return {
            "type": "pie",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": f"Pie chart showing proportional distribution of {num_field} by {cat_field}"
        }

    def _generate_scatter_plot(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a scatter plot specification"""
        if len(analysis["numerical_fields"]) < 2:
            return {"error": "Need at least 2 numerical fields for scatter plot"}

        x_field = analysis["numerical_fields"][0]
        y_field = analysis["numerical_fields"][1]

        fig = go.Figure()

        if isinstance(data[x_field], list) and isinstance(data[y_field], list):
            fig.add_trace(go.Scatter(
                x=data[x_field],
                y=data[y_field],
                mode='markers',
                name=f"{x_field} vs {y_field}"
            ))

        fig.update_layout(
            title=f"{y_field.title()} vs {x_field.title()}",
            xaxis_title=x_field.title(),
            yaxis_title=y_field.title(),
            template="plotly_white"
        )

        return {
            "type": "scatter",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": f"Scatter plot showing relationship between {x_field} and {y_field}"
        }

    def _generate_heatmap(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a heatmap specification"""
        if len(analysis["numerical_fields"]) < 3:
            return {"error": "Need at least 3 numerical fields for heatmap"}

        # Create correlation matrix
        numerical_data = {}
        for field in analysis["numerical_fields"][:5]:  # Limit to 5 fields
            if field in data and isinstance(data[field], list):
                numerical_data[field] = data[field]

        if len(numerical_data) < 2:
            return {"error": "Insufficient numerical data for heatmap"}

        df = pd.DataFrame(numerical_data)
        correlation_matrix = df.corr()

        fig = go.Figure()

        fig.add_trace(go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='RdBu',
            zmid=0
        ))

        fig.update_layout(
            title="Correlation Heatmap",
            template="plotly_white"
        )

        return {
            "type": "heatmap",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": "Heatmap showing correlations between numerical variables"
        }

    def _generate_visualization_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for data visualization"""
        recommendations = []

        if analysis["temporal_fields"]:
            recommendations.append("Consider time-series analysis for temporal trends")

        if len(analysis["categorical_fields"]) > 0:
            recommendations.append("Use bar or pie charts for categorical data distributions")

        if len(analysis["numerical_fields"]) >= 2:
            recommendations.append("Explore scatter plots to identify relationships between variables")

        if len(analysis["numerical_fields"]) >= 3:
            recommendations.append("Consider correlation analysis and heatmaps")

        if analysis["relationships"]:
            recommendations.append("Nested data structures may benefit from hierarchical visualizations")

        return recommendations


# Global instances
trend_predictor = CancerTrendPredictor()
graph_generator = LLMGraphGenerator()