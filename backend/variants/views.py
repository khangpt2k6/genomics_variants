from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404

from .models import Variant, ClinicalSignificance, DrugResponse, COSMICData, VariantAnnotation
from .serializers import (
    VariantSerializer, 
    ClinicalSignificanceSerializer, 
    DrugResponseSerializer,
    COSMICDataSerializer,
    VariantAnnotationSerializer,
    VariantDetailSerializer
)
from .filters import VariantFilter, ClinicalSignificanceFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class VariantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing genetic variants.
    Provides CRUD operations and advanced filtering.
    """
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VariantFilter
    search_fields = ['variant_id', 'gene_symbol', 'hgvs_c', 'hgvs_p', 'consequence']
    ordering_fields = ['chromosome', 'position', 'quality_score', 'gnomad_af', 'created_at']
    ordering = ['chromosome', 'position']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return VariantDetailSerializer
        return VariantSerializer

    @action(detail=True, methods=['get'])
    def annotations(self, request, pk=None):
        """Get all annotations for a specific variant"""
        variant = self.get_object()
        annotations = variant.annotations.all()
        serializer = VariantAnnotationSerializer(annotations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def clinical_significance(self, request, pk=None):
        """Get clinical significance data for a variant"""
        variant = self.get_object()
        clinical_data = variant.clinical_significance.all()
        serializer = ClinicalSignificanceSerializer(clinical_data, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def drug_responses(self, request, pk=None):
        """Get drug response data for a variant"""
        variant = self.get_object()
        drug_data = variant.drug_responses.all()
        serializer = DrugResponseSerializer(drug_data, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def cosmic_data(self, request, pk=None):
        """Get COSMIC data for a variant"""
        variant = self.get_object()
        cosmic_data = variant.cosmic_data.all()
        serializer = COSMICDataSerializer(cosmic_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get variant statistics"""
        queryset = self.filter_queryset(self.get_queryset())
        
        stats = {
            'total_variants': queryset.count(),
            'by_chromosome': dict(queryset.values_list('chromosome').annotate(count=Count('id'))),
            'by_impact': dict(queryset.values_list('impact').annotate(count=Count('id'))),
            'by_consequence': dict(queryset.values_list('consequence').annotate(count=Count('id'))),
            'average_quality': queryset.aggregate(avg_quality=Avg('quality_score'))['avg_quality'],
            'pathogenic_count': queryset.filter(clinical_significance__significance__in=['pathogenic', 'likely_pathogenic']).count(),
            'drug_target_count': queryset.filter(drug_responses__isnull=False).distinct().count(),
        }
        
        return Response(stats)

    @action(detail=False, methods=['get'])
    def search_by_gene(self, request):
        """Search variants by gene symbol"""
        gene_symbol = request.query_params.get('gene', '')
        if not gene_symbol:
            return Response({'error': 'Gene symbol parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        
        variants = self.queryset.filter(gene_symbol__iexact=gene_symbol)
        page = self.paginate_queryset(variants)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(variants, many=True)
        return Response(serializer.data)


class ClinicalSignificanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing clinical significance data.
    """
    queryset = ClinicalSignificance.objects.all()
    serializer_class = ClinicalSignificanceSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ClinicalSignificanceFilter
    search_fields = ['clinvar_id', 'phenotype', 'significance']
    ordering_fields = ['significance', 'review_date', 'created_at']
    ordering = ['-review_date']

    @action(detail=False, methods=['get'])
    def by_significance(self, request):
        """Get variants grouped by clinical significance"""
        significance = request.query_params.get('significance', '')
        if significance:
            queryset = self.queryset.filter(significance=significance)
        else:
            queryset = self.queryset.all()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AnnotationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing variant annotations.
    """
    queryset = VariantAnnotation.objects.all()
    serializer_class = VariantAnnotationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['variant__variant_id', 'variant__gene_symbol']
    ordering_fields = ['annotation_date', 'pathogenicity_score']
    ordering = ['-annotation_date']

    @action(detail=False, methods=['get'])
    def by_source(self, request):
        """Get annotations grouped by source"""
        source = request.query_params.get('source', '')
        if source:
            queryset = self.queryset.filter(source__name__icontains=source)
        else:
            queryset = self.queryset.all()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
