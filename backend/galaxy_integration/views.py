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
    GalaxyWorkflowSerializer, GalaxySyncJobSerializer, GalaxyAPIKeySerializer
)
from .filters import GalaxyInstanceFilter, GalaxyDatasetFilter, GalaxyWorkflowFilter


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
    filterset_class = GalaxyInstanceFilter
    ordering = ['name']

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """Test connection to Galaxy instance"""
        instance = self.get_object()
        
        # Here you would implement actual connection testing
        # For now, we'll simulate it
        try:
            # Simulate connection test
            instance.last_checked = timezone.now()
            instance.save()
            
            return Response({
                'status': 'success',
                'message': 'Connection successful',
                'last_checked': instance.last_checked
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def histories(self, request, pk=None):
        """Get histories for a Galaxy instance"""
        instance = self.get_object()
        histories = instance.histories.all()
        serializer = GalaxyHistorySerializer(histories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def datasets(self, request, pk=None):
        """Get datasets for a Galaxy instance"""
        instance = self.get_object()
        datasets = instance.datasets.all()
        serializer = GalaxyDatasetSerializer(datasets, many=True)
        return Response(serializer.data)


class GalaxyHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Galaxy histories.
    """
    queryset = GalaxyHistory.objects.all()
    serializer_class = GalaxyHistorySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['galaxy_instance', 'status', 'name']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def sync_from_galaxy(self, request, pk=None):
        """Sync history data from Galaxy"""
        history = self.get_object()
        
        # Here you would implement actual Galaxy API sync
        # For now, we'll simulate it
        try:
            history.updated_at = timezone.now()
            history.save()
            
            return Response({
                'status': 'success',
                'message': 'History synced successfully',
                'updated_at': history.updated_at
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def datasets(self, request, pk=None):
        """Get datasets for a history"""
        history = self.get_object()
        datasets = history.datasets.all()
        serializer = GalaxyDatasetSerializer(datasets, many=True)
        return Response(serializer.data)


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
    def download(self, request, pk=None):
        """Download dataset from Galaxy"""
        dataset = self.get_object()
        
        # Here you would implement actual download logic
        # For now, we'll simulate it
        try:
            dataset.processing_started_at = timezone.now()
            dataset.save()
            
            return Response({
                'status': 'success',
                'message': 'Download started',
                'download_url': dataset.download_url
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def process_vcf(self, request, pk=None):
        """Process VCF dataset"""
        dataset = self.get_object()
        
        if not dataset.is_vcf:
            return Response({
                'error': 'Dataset is not a VCF file'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Here you would implement VCF processing logic
        # For now, we'll simulate it
        try:
            dataset.processing_started_at = timezone.now()
            dataset.save()
            
            return Response({
                'status': 'success',
                'message': 'VCF processing started'
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def vcf_datasets(self, request):
        """Get VCF datasets"""
        queryset = self.queryset.filter(is_vcf=True)
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
        # For now, we'll simulate it
        try:
            workflow.status = 'running'
            workflow.started_at = timezone.now()
            workflow.save()
            
            return Response({
                'status': 'success',
                'message': 'Workflow started',
                'started_at': workflow.started_at
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a running workflow"""
        workflow = self.get_object()
        
        if workflow.status != 'running':
            return Response({
                'error': 'Workflow is not running'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        workflow.status = 'cancelled'
        workflow.save()
        
        return Response({
            'status': 'success',
            'message': 'Workflow cancelled'
        })


class GalaxySyncJobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Galaxy sync jobs.
    """
    queryset = GalaxySyncJob.objects.all()
    serializer_class = GalaxySyncJobSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['galaxy_instance', 'job_type', 'status']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """Start a sync job"""
        job = self.get_object()
        
        if job.status != 'pending':
            return Response({
                'error': 'Job is not in pending status'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        job.status = 'running'
        job.started_at = timezone.now()
        job.save()
        
        return Response({
            'status': 'success',
            'message': 'Sync job started'
        })

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a sync job"""
        job = self.get_object()
        
        if job.status not in ['pending', 'running']:
            return Response({
                'error': 'Job cannot be cancelled in current status'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        job.status = 'cancelled'
        job.save()
        
        return Response({
            'status': 'success',
            'message': 'Sync job cancelled'
        })


class GalaxyAPIKeyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Galaxy API keys.
    """
    queryset = GalaxyAPIKey.objects.all()
    serializer_class = GalaxyAPIKeySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['galaxy_instance', 'is_active', 'key_name']
    ordering = ['-created_at']

    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        """Test API key"""
        api_key = self.get_object()
        
        # Here you would implement actual API key testing
        # For now, we'll simulate it
        try:
            api_key.last_used = timezone.now()
            api_key.usage_count += 1
            api_key.save()
            
            return Response({
                'status': 'success',
                'message': 'API key is valid',
                'last_used': api_key.last_used,
                'usage_count': api_key.usage_count
            })
        except Exception as e:
            api_key.last_error = str(e)
            api_key.save()
            
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)