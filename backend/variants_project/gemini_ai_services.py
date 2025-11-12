import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

from .gemini_service import GeminiService
from variants.models import Variant, ClinicalSignificance, DrugResponse, CancerTrendPrediction

logger = logging.getLogger(__name__)


class GeminiTrendPredictor(GeminiService):
    
    def predict_variant_trends(self, days_ahead: int = 30) -> Dict[str, Any]:
        try:
            historical_data = self._get_historical_variant_data()
            
            if not historical_data or len(historical_data) < 7:
                return {"error": "Insufficient historical data for prediction. Need at least 7 data points."}
            
            trend_analysis = self._analyze_trends_with_gemini(historical_data)
            predictions = self._generate_predictions(historical_data, days_ahead)
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
        six_months_ago = datetime.now() - timedelta(days=180)
        
        variants = Variant.objects.filter(
            created_at__gte=six_months_ago
        ).order_by('created_at')
        
        historical_data = []
        for variant in variants:
            data_point = {
                'date': variant.created_at.date().isoformat(),
                'chromosome': variant.chromosome,
                'gene': variant.gene_symbol or 'Unknown',
                'impact': variant.impact or 'UNKNOWN',
                'gnomad_af': float(variant.gnomad_af) if variant.gnomad_af else 0.0,
                'clinical_significance': None,
                'drug_responses': []
            }
            
            clin_sig = ClinicalSignificance.objects.filter(variant=variant).first()
            if clin_sig:
                data_point['clinical_significance'] = clin_sig.significance
            
            drug_responses = DrugResponse.objects.filter(variant=variant)
            data_point['drug_responses'] = [
                {
                    'drug': dr.drug_name,
                    'response_type': dr.response_type,
                    'evidence_level': dr.evidence_level
                } for dr in drug_responses[:3]
            ]
            
            historical_data.append(data_point)
        
        return historical_data
    
    def _analyze_trends_with_gemini(self, historical_data: List[Dict]) -> Dict[str, Any]:
        data_summary = self._prepare_data_summary(historical_data)
        
        prompt = f"""Analyze the following cancer variant data trends and provide insights in JSON format:

{data_summary}

Provide a JSON response with these keys:
- key_trends: array of 3-5 key trends
- significant_genes: array of top 5 genes showing increased variant frequency
- clinical_patterns: array of clinical significance patterns observed
- drug_implications: array of drug response implications
- risk_assessment: string describing risk level (low/medium/high)
- recommendations: array of 3-5 recommendations for monitoring

Return ONLY valid JSON, no markdown or extra text."""

        try:
            response_text = self.generate_text(prompt, temperature=0.3, max_tokens=2048)
            
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            logger.warning(f"Failed to parse Gemini response as JSON: {e}")
            return {
                "key_trends": ["Analysis completed but formatting issue occurred"],
                "significant_genes": [],
                "clinical_patterns": [],
                "drug_implications": [],
                "risk_assessment": "Unable to assess",
                "recommendations": ["Review data manually"]
            }
    
    def _prepare_data_summary(self, historical_data: List[Dict]) -> str:
        df = pd.DataFrame(historical_data)
        
        if df.empty:
            return "No data available for analysis"
        
        daily_stats = df.groupby('date').agg({
            'gene': 'count',
            'impact': lambda x: x.value_counts().to_dict() if len(x.value_counts()) > 0 else {}
        }).reset_index()
        
        gene_freq = df['gene'].value_counts().head(10).to_dict()
        impact_dist = df['impact'].value_counts().to_dict()
        
        summary = f"""
Historical Data Summary:
- Total variants analyzed: {len(df)}
- Date range: {df['date'].min()} to {df['date'].max()}
- Daily average variants: {len(df) / len(daily_stats):.1f}

Top Genes by Frequency:
{json.dumps(gene_freq, indent=2)}

Impact Distribution:
{json.dumps(impact_dist, indent=2)}

Recent Trends (last 30 days):
- Average daily variants: {len(df[df['date'] >= (datetime.now() - timedelta(days=30)).date().isoformat()]) / max(1, 30):.1f}
"""
        
        return summary
    
    def _generate_predictions(self, historical_data: List[Dict], days_ahead: int) -> Dict[str, Any]:
        df = pd.DataFrame(historical_data)
        
        if df.empty or len(df) < 7:
            return {"error": "Insufficient data for prediction"}
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        daily_counts = df.groupby('date').size().reset_index(name='count')
        
        unique_dates = daily_counts['date'].nunique()
        if unique_dates < 2:
            avg_daily = daily_counts['count'].sum() / max(1, unique_dates)
            return {
                "predicted_counts": [avg_daily] * days_ahead,
                "future_dates": [(datetime.now() + timedelta(days=i+1)).date().isoformat() for i in range(days_ahead)],
                "trend_direction": "stable",
                "confidence_interval": [[max(0, avg_daily * 0.8), avg_daily * 1.2]] * days_ahead
            }
        
        date_range = pd.date_range(start=daily_counts['date'].min(),
                                 end=daily_counts['date'].max())
        daily_counts = daily_counts.set_index('date').reindex(date_range, fill_value=0).reset_index()
        daily_counts.columns = ['date', 'count']
        
        daily_counts['days_since_start'] = (daily_counts['date'] - daily_counts['date'].min()).dt.days
        
        X = daily_counts[['days_since_start']].values
        y = daily_counts['count'].values
        
        if len(X) < 2:
            avg_daily = y.mean() if len(y) > 0 else 0
            return {
                "predicted_counts": [avg_daily] * days_ahead,
                "future_dates": [(datetime.now() + timedelta(days=i+1)).date().isoformat() for i in range(days_ahead)],
                "trend_direction": "stable",
                "confidence_interval": [[max(0, avg_daily * 0.8), avg_daily * 1.2]] * days_ahead
            }
        
        try:
            from sklearn.linear_model import LinearRegression
            model = LinearRegression()
            model.fit(X, y)
        except ImportError:
            return {"error": "scikit-learn is required. Install with: pip install scikit-learn"}
        
        future_dates = pd.date_range(start=daily_counts['date'].max() + timedelta(days=1),
                                   periods=days_ahead)
        future_days = np.arange(len(daily_counts), len(daily_counts) + days_ahead).reshape(-1, 1)
        
        predictions = model.predict(future_days)
        predictions = np.maximum(predictions, 0)
        
        slope = model.coef_[0] if len(model.coef_) > 0 else 0
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
        intervals = []
        for pred in predictions:
            intervals.append([max(0, pred - historical_std), pred + historical_std])
        return intervals
    
    def _create_trend_visualizations(self, historical_data: List[Dict], predictions: Dict) -> Dict[str, Any]:
        df = pd.DataFrame(historical_data)
        df['date'] = pd.to_datetime(df['date'])
        
        charts = {}
        
        daily_counts = df.groupby('date').size().reset_index(name='count')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=daily_counts['date'],
            y=daily_counts['count'],
            mode='lines+markers',
            name='Historical Data',
            line=dict(color='#000000', width=2)
        ))
        
        if 'future_dates' in predictions and 'predicted_counts' in predictions:
            future_dates = pd.to_datetime(predictions['future_dates'])
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=predictions['predicted_counts'],
                mode='lines',
                name='Predictions',
                line=dict(color='#ef4444', dash='dash', width=2)
            ))
        
        fig.update_layout(
            title="Cancer Variant Discovery Trends",
            xaxis_title="Date",
            yaxis_title="Number of Variants",
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        charts['trend_chart'] = json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))
        
        gene_counts = df['gene'].value_counts().head(10)
        fig2 = px.bar(
            x=gene_counts.index,
            y=gene_counts.values,
            title="Top 10 Genes by Variant Frequency",
            labels={'x': 'Gene', 'y': 'Variant Count'}
        )
        fig2.update_layout(
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        charts['gene_chart'] = json.loads(json.dumps(fig2, cls=PlotlyJSONEncoder))
        
        return charts
    
    def _calculate_confidence_score(self, historical_data: List[Dict]) -> float:
        if len(historical_data) < 14:
            return 0.3
        elif len(historical_data) < 30:
            return 0.6
        elif len(historical_data) < 90:
            return 0.8
        else:
            return 0.9


class GeminiGraphGenerator(GeminiService):
    
    def generate_graph_from_data(self, data: Dict[str, Any], graph_type: str = "auto") -> Dict[str, Any]:
        try:
            data_analysis = self._analyze_data_structure(data)
            
            if graph_type == "auto":
                recommended_graphs = self._recommend_graph_types(data_analysis)
            else:
                recommended_graphs = [graph_type]
            
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
        recommendations = []
        
        num_numerical = len(data_analysis["numerical_fields"])
        num_categorical = len(data_analysis["categorical_fields"])
        
        if data_analysis["temporal_fields"]:
            recommendations.append("line")
        
        if num_categorical > 0:
            recommendations.append("bar")
        
        if num_categorical == 1 and num_numerical >= 1:
            recommendations.append("pie")
        
        if num_numerical >= 2:
            recommendations.append("scatter")
        
        if num_numerical >= 3:
            recommendations.append("heatmap")
        
        if not recommendations:
            recommendations = ["bar"]
        
        return recommendations[:3]
    
    def _generate_specific_graph(self, data: Dict[str, Any], graph_type: str, analysis: Dict[str, Any]) -> Dict[str, Any]:
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
            return self._generate_bar_chart(data, analysis)
    
    def _generate_bar_chart(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        cat_field = analysis["categorical_fields"][0] if analysis["categorical_fields"] else None
        num_field = analysis["numerical_fields"][0] if analysis["numerical_fields"] else None
        
        if not cat_field or not num_field:
            return {"error": "Insufficient data for bar chart"}
        
        fig = go.Figure()
        
        if isinstance(data[cat_field], list) and isinstance(data[num_field], list):
            fig.add_trace(go.Bar(
                x=data[cat_field],
                y=data[num_field],
                name=num_field.title(),
                marker_color='#000000'
            ))
        
        fig.update_layout(
            title=f"{num_field.title()} by {cat_field.title()}",
            xaxis_title=cat_field.title(),
            yaxis_title=num_field.title(),
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return {
            "type": "bar",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": f"Bar chart showing {num_field} distribution across {cat_field} categories"
        }
    
    def _generate_line_chart(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        x_field = None
        y_field = analysis["numerical_fields"][0] if analysis["numerical_fields"] else None
        
        for field in analysis["temporal_fields"]:
            if field in data:
                x_field = field
                break
        
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
                name=y_field.title(),
                line=dict(color='#000000', width=2)
            ))
        
        fig.update_layout(
            title=f"{y_field.title()} Over Time",
            xaxis_title=x_field.title(),
            yaxis_title=y_field.title(),
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return {
            "type": "line",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": f"Line chart showing {y_field} trends over {x_field}"
        }
    
    def _generate_pie_chart(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
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
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return {
            "type": "pie",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": f"Pie chart showing proportional distribution of {num_field} by {cat_field}"
        }
    
    def _generate_scatter_plot(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
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
                name=f"{x_field} vs {y_field}",
                marker=dict(color='#000000', size=8)
            ))
        
        fig.update_layout(
            title=f"{y_field.title()} vs {x_field.title()}",
            xaxis_title=x_field.title(),
            yaxis_title=y_field.title(),
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return {
            "type": "scatter",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": f"Scatter plot showing relationship between {x_field} and {y_field}"
        }
    
    def _generate_heatmap(self, data: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        if len(analysis["numerical_fields"]) < 3:
            return {"error": "Need at least 3 numerical fields for heatmap"}
        
        numerical_data = {}
        for field in analysis["numerical_fields"][:5]:
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
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return {
            "type": "heatmap",
            "data": json.loads(json.dumps(fig, cls=PlotlyJSONEncoder)),
            "description": "Heatmap showing correlations between numerical variables"
        }
    
    def _generate_visualization_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
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


_trend_predictor = None
_graph_generator = None

def get_trend_predictor():
    global _trend_predictor
    if _trend_predictor is None:
        try:
            _trend_predictor = GeminiTrendPredictor()
        except Exception as e:
            logger.error(f"Failed to initialize GeminiTrendPredictor: {str(e)}")
            raise ValueError(f"Failed to initialize trend predictor: {str(e)}. Check GEMINI_API_KEY is set.")
    return _trend_predictor

def get_graph_generator():
    global _graph_generator
    if _graph_generator is None:
        try:
            _graph_generator = GeminiGraphGenerator()
        except Exception as e:
            logger.error(f"Failed to initialize GeminiGraphGenerator: {str(e)}")
            raise ValueError(f"Failed to initialize graph generator: {str(e)}. Check GEMINI_API_KEY is set.")
    return _graph_generator

