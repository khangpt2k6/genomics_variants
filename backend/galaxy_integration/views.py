from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    GalaxyInstance, GalaxyHistory, GalaxyDataset, GalaxyWorkflow,
    GalaxySyncJob, GalaxyAPIKey
)
from .serializers import (
    GalaxyInstanceSerializer, GalaxyHistorySerializer, GalaxyDatasetSerializer,
    GalaxyWorkflowSerializer, GalaxySyncJobSerializer, GalaxyAPIKeySerializer,
    GalaxyInstanceCreateSerializer, GalaxyDatasetProcessSerializer,
    GalaxySyncJobCreateSerializer, GalaxyStatisticsSerializer
)
from .filters import (
    GalaxyHistoryFilter, GalaxyDatasetFilter, GalaxyWorkflowFilter,
    GalaxySyncJobFilter, GalaxyDatasetSearchFilter
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class GalaxyInstanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Galaxy instances.
    """
    queryset = GalaxyInstance.objects.all()
    serializer_class = GalaxyInstanceSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'is_active']
    ordering = ['name']

    def get_serializer_class(self):
        if self.action == 'create':
            return GalaxyInstanceCreateSerializer
        return GalaxyInstanceSerializer

    @action(detail=True, methods=['get'])
    def test_connection(self, request, pk=None):
        """Test connection to Galaxy instance"""
        instance = self.get_object()
        # Here you would implement actual connection testing
        # For now, return a mock response
        return Response({
            'status': 'success',
            'message': f'Connection to {instance.name} successful',
            'galaxy_version': '21.09',
            'last_checked': timezone.now()
        })

    @action(detail=True, methods=['post'])
    def sync_histories(self, request, pk=None):
        """Sync histories from Galaxy instance"""
        instance = self.get_object()
        # Here you would implement actual history syncing
        return Response({
            'status': 'started',
            'message': f'History sync started for {instance.name}'
        })

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics for Galaxy instance"""
        instance = self.get_object()
        
        stats = {
            'histories_count': instance.histories.count(),
            'datasets_count': instance.datasets.count(),
            'workflows_count': instance.workflows.count(),
            'vcf_datasets_count': instance.datasets.filter(is_vcf=True).count(),
            'processed_datasets_count': instance.datasets.filter(is_processed=True).count(),
            'last_sync': instance.last_checked,
        }
        
        return Response(stats)


class GalaxyHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Galaxy histories.
    """
    queryset = GalaxyHistory.objects.all()
    serializer_class = GalaxyHistorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = GalaxyHistoryFilter
    ordering = ['-created_at']

    @action(detail=True, methods=['get'])
    def datasets(self, request, pk=None):
        """Get datasets for a specific history"""
        history = self.get_object()
        datasets = history.datasets.all()
        serializer = GalaxyDatasetSerializer(datasets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def sync_datasets(self, request, pk=None):
        """Sync datasets for a specific history"""
        history = self.get_object()
        # Here you would implement actual dataset syncing
        return Response({
            'status': 'started',
            'message': f'Dataset sync started for history {history.name}'
        })


class GalaxyDatasetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Galaxy datasets.
    """
    queryset = GalaxyDataset.objects.all()
    serializer_class = GalaxyDatasetSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = GalaxyDatasetFilter
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process a Galaxy dataset"""
        dataset = self.get_object()
        serializer = GalaxyDatasetProcessSerializer(data=request.data)
        
        if serializer.is_valid():
            # Here you would implement actual dataset processing
            dataset.is_processed = True
            dataset.processing_started_at = timezone.now()
            dataset.processing_completed_at = timezone.now()
            dataset.save()
            
            return Response({
                'status': 'success',
                'message': f'Dataset {dataset.name} processed successfully'
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Get download URL for dataset"""
        dataset = self.get_object()
        if not dataset.download_url:
            return Response(
                {'error': 'Download URL not available'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({'download_url': dataset.download_url})

    @action(detail=False, methods=['get'])
    def vcf_datasets(self, request):
        """Get all VCF datasets"""
        queryset = self.queryset.filter(is_vcf=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unprocessed(self, request):
        """Get unprocessed datasets"""
        queryset = self.queryset.filter(is_processed=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GalaxyWorkflowViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Galaxy workflows.
    """
    queryset = GalaxyWorkflow.objects.all()
    serializer_class = GalaxyWorkflowSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = GalaxyWorkflowFilter
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        """Run a Galaxy workflow"""
        workflow = self.get_object()
        # Here you would implement actual workflow execution
        workflow.status = 'running'
        workflow.started_at = timezone.now()
        workflow.save()
        
        return Response({
            'status': 'started',
            'message': f'Workflow {workflow.name} started'
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a running workflow"""
        workflow = self.get_object()
        if workflow.status != 'running':
            return Response(
                {'error': 'Workflow is not running'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        workflow.status = 'cancelled'
        workflow.save()
        
        return Response({'status': 'cancelled'})


class GalaxySyncJobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Galaxy sync jobs.
    """
    queryset = GalaxySyncJob.objects.all()
    serializer_class = GalaxySyncJobSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = GalaxySyncJobFilter
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return GalaxySyncJobCreateSerializer
        return GalaxySyncJobSerializer

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a sync job"""
        job = self.get_object()
        if job.status != 'pending':
            return Response(
                {'error': 'Job is not in pending status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        job.status = 'running'
        job.started_at = timezone.now()
        job.save()
        
        return Response({'status': 'started'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a sync job"""
        job = self.get_object()
        if job.status not in ['pending', 'running']:
            return Response(
                {'error': 'Job cannot be cancelled in current status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        job.status = 'cancelled'
        job.save()
        
        return Response({'status': 'cancelled'})


class GalaxyAPIKeyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Galaxy API keys.
    """
    queryset = GalaxyAPIKey.objects.all()
    serializer_class = GalaxyAPIKeySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['galaxy_instance', 'is_active']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """Test API key"""
        api_key = self.get_object()
        # Here you would implement actual API key testing
        api_key.last_used = timezone.now()
        api_key.usage_count += 1
        api_key.save()
        
        return Response({
            'status': 'valid',
            'message': f'API key {api_key.key_name} is valid'
        })


class GalaxyStatisticsViewSet(viewsets.ViewSet):
    """
    ViewSet for Galaxy statistics.
    """
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get overall Galaxy statistics"""
        stats = {
            'total_instances': GalaxyInstance.objects.count(),
            'active_instances': GalaxyInstance.objects.filter(is_active=True).count(),
            'total_histories': GalaxyHistory.objects.count(),
            'total_datasets': GalaxyDataset.objects.count(),
            'vcf_datasets': GalaxyDataset.objects.filter(is_vcf=True).count(),
            'processed_datasets': GalaxyDataset.objects.filter(is_processed=True).count(),
            'total_workflows': GalaxyWorkflow.objects.count(),
            'running_workflows': GalaxyWorkflow.objects.filter(status='running').count(),
            'total_sync_jobs': GalaxySyncJob.objects.count(),
            'active_sync_jobs': GalaxySyncJob.objects.filter(status='running').count(),
        }
        
        serializer = GalaxyStatisticsSerializer(stats)
        return Response(serializer.data)
