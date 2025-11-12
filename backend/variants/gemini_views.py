from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Variant
from .serializers import VariantSerializer
from variants_project.gemini_service import (
    get_variant_interpreter,
    get_query_processor,
    get_chat_assistant,
    get_annotation_enhancer
)


class VariantLLMViewSet(viewsets.ViewSet):
    
    @action(detail=True, methods=['get'])
    def explain(self, request, pk=None):
        variant = get_object_or_404(Variant, pk=pk)
        
        try:
            interpreter = get_variant_interpreter()
            result = interpreter.generate_variant_summary(variant)
            return Response(result)
        except Exception as e:
            return Response(
                {"error": f"Failed to generate explanation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def clinical_explanation(self, request, pk=None):
        variant = get_object_or_404(Variant, pk=pk)
        
        try:
            interpreter = get_variant_interpreter()
            explanation = interpreter.explain_clinical_significance(variant)
            return Response({
                "variant_id": variant.variant_id,
                "explanation": explanation
            })
        except Exception as e:
            return Response(
                {"error": f"Failed to generate clinical explanation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def patient_summary(self, request, pk=None):
        variant = get_object_or_404(Variant, pk=pk)
        
        try:
            interpreter = get_variant_interpreter()
            summary = interpreter.generate_patient_friendly_summary(variant)
            return Response({
                "variant_id": variant.variant_id,
                "summary": summary
            })
        except Exception as e:
            return Response(
                {"error": f"Failed to generate patient summary: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def enhance_annotations(self, request, pk=None):
        variant = get_object_or_404(Variant, pk=pk)
        include_literature = request.data.get('include_literature', True)
        include_pathways = request.data.get('include_pathways', True)
        
        try:
            enhancer = get_annotation_enhancer()
            enhancements = {}
            
            if include_literature:
                enhancements['literature_context'] = enhancer.enhance_with_literature_context(variant)
            
            if include_pathways:
                enhancements['pathway_analysis'] = enhancer.generate_pathway_analysis(variant)
            
            return Response({
                "variant_id": variant.variant_id,
                "enhancements": enhancements
            })
        except Exception as e:
            return Response(
                {"error": f"Failed to enhance annotations: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class NaturalLanguageSearchView(APIView):
    
    def post(self, request):
        query = request.data.get('query', '')
        
        if not query:
            return Response(
                {"error": "Query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            processor = get_query_processor()
            
            available_fields = [
                'chromosome', 'position', 'gene_symbol', 'impact', 'consequence',
                'gnomad_af', 'quality_score', 'clinical_significance__significance',
                'drug_responses__drug_name', 'drug_responses__response_type'
            ]
            
            result = processor.process_query(query, available_fields)
            
            queryset = Variant.objects.all()
            filters = result.get('filters', {})
            
            q_objects = Q()
            for field, filter_data in filters.items():
                operator = filter_data.get('operator', 'exact')
                value = filter_data.get('value')
                
                if operator == 'exact':
                    q_objects &= Q(**{field: value})
                elif operator == 'contains':
                    q_objects &= Q(**{f"{field}__icontains": value})
                elif operator == 'in':
                    q_objects &= Q(**{f"{field}__in": value})
                elif operator == 'lt':
                    q_objects &= Q(**{f"{field}__lt": value})
                elif operator == 'gt':
                    q_objects &= Q(**{f"{field}__gt": value})
            
            search_terms = result.get('search_terms', [])
            if search_terms:
                search_q = Q()
                for term in search_terms:
                    search_q |= Q(gene_symbol__icontains=term) | \
                               Q(variant_id__icontains=term) | \
                               Q(consequence__icontains=term)
                q_objects &= search_q
            
            variants = queryset.filter(q_objects).distinct()[:100]
            
            serializer = VariantSerializer(variants, many=True)
            
            return Response({
                "query": query,
                "interpretation": result.get('interpretation', ''),
                "filters_applied": filters,
                "results_count": variants.count(),
                "results": serializer.data
            })
            
        except Exception as e:
            return Response(
                {"error": f"Failed to process query: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get(self, request):
        partial_query = request.query_params.get('q', '')
        
        if not partial_query:
            return Response(
                {"error": "Query parameter 'q' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            processor = get_query_processor()
            suggestions = processor.suggest_queries(partial_query)
            
            return Response({
                "partial_query": partial_query,
                "suggestions": suggestions
            })
        except Exception as e:
            return Response(
                {"error": f"Failed to generate suggestions: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VariantChatView(APIView):
    
    def post(self, request):
        message = request.data.get('message', '')
        variant_id = request.data.get('variant_id')
        
        if not message:
            return Response(
                {"error": "Message parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            assistant = get_chat_assistant()
            
            variant_context = None
            if variant_id:
                try:
                    variant_context = Variant.objects.get(variant_id=variant_id)
                except Variant.DoesNotExist:
                    pass
            
            response = assistant.chat(message, variant_context)
            
            return Response({
                "message": message,
                "response": response,
                "variant_context": variant_context.variant_id if variant_context else None
            })
        except Exception as e:
            return Response(
                {"error": f"Failed to process chat message: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def delete(self, request):
        try:
            assistant = get_chat_assistant()
            assistant.reset_conversation()
            return Response({"message": "Conversation history reset"})
        except Exception as e:
            return Response(
                {"error": f"Failed to reset conversation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
