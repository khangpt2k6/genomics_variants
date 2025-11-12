from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json
import logging

from variants_project.gemini_ai_services import get_trend_predictor, get_graph_generator
from variants.models import Variant, CancerTrendPrediction
from django.utils import timezone

logger = logging.getLogger(__name__)


class TrendPredictionView(APIView):
    
    def post(self, request):
        try:
            days_ahead = int(request.data.get('days_ahead', 30))
            
            if days_ahead < 1 or days_ahead > 365:
                return Response(
                    {'error': 'days_ahead must be between 1 and 365'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            trend_predictor = get_trend_predictor()
            result = trend_predictor.predict_variant_trends(days_ahead=days_ahead)
            
            if 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
            prediction = CancerTrendPrediction.objects.create(
                prediction_id=f"pred_{timezone.now().strftime('%Y%m%d_%H%M%S')}",
                prediction_horizon_days=days_ahead,
                trend_direction=result['predictions'].get('trend_direction', 'stable'),
                confidence_score=result.get('confidence_score', 0.5),
                predicted_variant_counts=result['predictions'].get('predicted_counts', []),
                prediction_dates=result['predictions'].get('future_dates', []),
                confidence_intervals=result['predictions'].get('confidence_interval', []),
                key_trends=result['analysis'].get('key_trends', []),
                significant_genes=result['analysis'].get('significant_genes', []),
                clinical_patterns=result['analysis'].get('clinical_patterns', []),
                drug_implications=result['analysis'].get('drug_implications', []),
                risk_assessment=result['analysis'].get('risk_assessment', 'unknown'),
                recommendations=result['analysis'].get('recommendations', []),
                trend_chart_data=result['charts'].get('trend_chart', {}),
                gene_chart_data=result['charts'].get('gene_chart', {}),
                total_variants_analyzed=Variant.objects.count()
            )
            
            return Response({
                'prediction_id': prediction.prediction_id,
                'predictions': result['predictions'],
                'analysis': result['analysis'],
                'charts': result['charts'],
                'confidence_score': result['confidence_score'],
                'created_at': prediction.created_at.isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error in trend prediction: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        try:
            predictions = CancerTrendPrediction.objects.all().order_by('-created_at')[:10]
            
            return Response({
                'predictions': [
                    {
                        'prediction_id': p.prediction_id,
                        'trend_direction': p.trend_direction,
                        'confidence_score': p.confidence_score,
                        'prediction_horizon_days': p.prediction_horizon_days,
                        'created_at': p.created_at.isoformat(),
                        'key_trends': p.key_trends[:3] if p.key_trends else [],
                        'risk_assessment': p.risk_assessment
                    }
                    for p in predictions
                ]
            })
        except Exception as e:
            logger.error(f"Error getting trend predictions: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GraphGenerationView(APIView):
    
    def post(self, request):
        try:
            data = request.data.get('data')
            graph_type = request.data.get('graph_type', 'auto')
            
            if not data:
                return Response(
                    {'error': 'Data is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if not isinstance(data, dict):
                return Response(
                    {'error': 'Data must be a dictionary/object'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            graph_generator = get_graph_generator()
            result = graph_generator.generate_graph_from_data(data, graph_type=graph_type)
            
            if 'error' in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(result)
            
        except Exception as e:
            logger.error(f"Error in graph generation: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VariantStatisticsGraphView(APIView):
    
    def get(self, request):
        try:
            variants = Variant.objects.all()[:1000]
            
            impact_counts = {}
            gene_counts = {}
            chromosome_counts = {}
            
            for variant in variants:
                if variant.impact:
                    impact_counts[variant.impact] = impact_counts.get(variant.impact, 0) + 1
                
                if variant.gene_symbol:
                    gene_counts[variant.gene_symbol] = gene_counts.get(variant.gene_symbol, 0) + 1
                
                if variant.chromosome:
                    chromosome_counts[variant.chromosome] = chromosome_counts.get(variant.chromosome, 0) + 1
            
            data = {
                'impacts': list(impact_counts.keys()),
                'impact_counts': list(impact_counts.values()),
                'genes': list(gene_counts.keys())[:20],
                'gene_counts': list(gene_counts.values())[:20],
                'chromosomes': list(chromosome_counts.keys()),
                'chromosome_counts': list(chromosome_counts.values())
            }
            
            graph_generator = get_graph_generator()
            result = graph_generator.generate_graph_from_data(data, graph_type='auto')
            
            return Response(result)
            
        except Exception as e:
            logger.error(f"Error generating variant statistics graph: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

