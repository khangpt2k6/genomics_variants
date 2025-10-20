from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    AnnotationSource, AnnotationJob, VariantAnnotation, 
    ClinVarAnnotation, COSMICAnnotation, CIViCAnnotation, AnnotationCache
)
from .serializers import (
    AnnotationSourceSerializer, AnnotationJobSerializer, VariantAnnotationSerializer,
    ClinVarAnnotationSerializer, COSMICAnnotationSerializer, CIViCAnnotationSerializer,
    AnnotationCacheSerializer
)
from .filters import AnnotationJobFilter, VariantAnnotationFilter


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class AnnotationSourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing annotation sources.
    """
    queryset = AnnotationSource.objects.all()
    serializer_class = AnnotationSourceSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'is_active']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def jobs(self, request, pk=None):
        """Get annotation jobs for a specific source"""
        source = self.get_object()
        jobs = source.annotationjob_set.all()
        serializer = AnnotationJobSerializer(jobs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def create_job(self, request, pk=None):
        """Create a new annotation job for this source"""
        source = self.get_object()
        job_data = request.data.copy()
        job_data['source'] = source.id
        
        serializer = AnnotationJobSerializer(data=job_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnnotationJobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing annotation jobs.
    """
    queryset = AnnotationJob.objects.all()
    serializer_class = AnnotationJobSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnnotationJobFilter
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start an annotation job"""
        job = self.get_object()
        if job.status != 'pending':
            return Response(
                {'error': 'Job is not in pending status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        job.status = 'running'
        job.started_at = timezone.now()
        job.save()
        
        # Here you would typically start the actual annotation process
        # For now, we'll just update the status
        
        return Response({'status': 'Job started'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an annotation job"""
        job = self.get_object()
        if job.status not in ['pending', 'running']:
            return Response(
                {'error': 'Job cannot be cancelled in current status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        job.status = 'cancelled'
        job.save()
        
        return Response({'status': 'Job cancelled'})

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get job progress information"""
        job = self.get_object()
        
        progress = {
            'status': job.status,
            'processed_count': job.processed_count,
            'total_count': job.variant_count,
            'failed_count': job.failed_count,
            'progress_percentage': (job.processed_count / job.variant_count * 100) if job.variant_count > 0 else 0,
            'started_at': job.started_at,
            'completed_at': job.completed_at,
            'error_message': job.error_message
        }
        
        return Response(progress)


class VariantAnnotationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing variant annotations.
    """
    queryset = VariantAnnotation.objects.all()
    serializer_class = VariantAnnotationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = VariantAnnotationFilter
    ordering = ['-annotation_date']

    @action(detail=False, methods=['get'])
    def by_variant(self, request):
        """Get annotations for a specific variant"""
        variant_id = request.query_params.get('variant_id')
        if not variant_id:
            return Response(
                {'error': 'variant_id parameter required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        annotations = self.queryset.filter(variant_id=variant_id)
        page = self.paginate_queryset(annotations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(annotations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_source(self, request):
        """Get annotations from a specific source"""
        source_name = request.query_params.get('source')
        if not source_name:
            return Response(
                {'error': 'source parameter required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        annotations = self.queryset.filter(source__name__icontains=source_name)
        page = self.paginate_queryset(annotations)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(annotations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get annotation statistics"""
        queryset = self.filter_queryset(self.get_queryset())
        
        stats = {
            'total_annotations': queryset.count(),
            'successful_annotations': queryset.filter(is_successful=True).count(),
            'failed_annotations': queryset.filter(is_successful=False).count(),
            'by_source': dict(queryset.values_list('source__name').annotate(count=Count('id'))),
            'average_confidence': queryset.aggregate(avg_confidence=Avg('confidence_score'))['avg_confidence'],
        }
        
        return Response(stats)


class ClinVarAnnotationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing ClinVar annotations.
    """
    queryset = ClinVarAnnotation.objects.all()
    serializer_class = ClinVarAnnotationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['clinical_significance', 'review_status', 'clinvar_id']
    ordering = ['-review_date']

    @action(detail=False, methods=['get'])
    def by_significance(self, request):
        """Get annotations grouped by clinical significance"""
        significance = request.query_params.get('significance', '')
        if significance:
            queryset = self.queryset.filter(clinical_significance__icontains=significance)
        else:
            queryset = self.queryset.all()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class COSMICAnnotationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing COSMIC annotations.
    """
    queryset = COSMICAnnotation.objects.all()
    serializer_class = COSMICAnnotationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['primary_site', 'primary_histology', 'cosmic_id']
    ordering = ['cosmic_id']

    @action(detail=False, methods=['get'])
    def by_cancer_type(self, request):
        """Get annotations grouped by cancer type"""
        cancer_type = request.query_params.get('cancer_type', '')
        if cancer_type:
            queryset = self.queryset.filter(
                Q(primary_site__icontains=cancer_type) | 
                Q(primary_histology__icontains=cancer_type)
            )
        else:
            queryset = self.queryset.all()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CIViCAnnotationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing CIViC annotations.
    """
    queryset = CIViCAnnotation.objects.all()
    serializer_class = CIViCAnnotationSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['drug_name', 'response_type', 'evidence_level', 'cancer_type']
    ordering = ['drug_name', 'evidence_level']

    @action(detail=False, methods=['get'])
    def by_drug(self, request):
        """Get annotations grouped by drug"""
        drug_name = request.query_params.get('drug_name', '')
        if drug_name:
            queryset = self.queryset.filter(drug_name__icontains=drug_name)
        else:
            queryset = self.queryset.all()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AnnotationCacheViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing annotation cache.
    """
    queryset = AnnotationCache.objects.all()
    serializer_class = AnnotationCacheSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['variant', 'cache_key']
    ordering = ['-created_at']

    @action(detail=False, methods=['post'])
    def clear_expired(self, request):
        """Clear expired cache entries"""
        from django.utils import timezone
        
        expired_count = AnnotationCache.objects.filter(
            expires_at__lt=timezone.now()
        ).count()
        
        AnnotationCache.objects.filter(
            expires_at__lt=timezone.now()
        ).delete()
        
        return Response({'cleared_count': expired_count})

    @action(detail=False, methods=['post'])
    def clear_all(self, request):
        """Clear all cache entries"""
        total_count = AnnotationCache.objects.count()
        AnnotationCache.objects.all().delete()
        
        return Response({'cleared_count': total_count})
