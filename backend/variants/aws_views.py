from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import logging
from variants_project.s3_storage import s3_storage
from variants_project.sqs_handlers import sqs_handler
from annotations.models import AnnotationJob, AnnotationSource
from galaxy_integration.models import GalaxySyncJob
from .serializers import VariantSerializer

logger = logging.getLogger(__name__)


class AWSFileUploadViewSet(viewsets.ViewSet):
    """ViewSet for handling file uploads to AWS S3"""
    
    parser_classes = (MultiPartParser, FormParser)
    
    @action(detail=False, methods=['post'])
    def upload_vcf(self, request):
        """Upload VCF file to S3 and queue for processing"""
        if not settings.USE_AWS:
            return Response(
                {'error': 'AWS services not enabled'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        file = request.FILES.get('file')
        if not file:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not file.name.endswith('.vcf') and not file.name.endswith('.vcf.gz'):
            return Response(
                {'error': 'Only VCF files are supported'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = s3_storage.upload_vcf_file(
                file,
                file.name,
                metadata={
                    'file_size': file.size,
                    'content_type': file.content_type
                }
            )
            
            if result['success']:
                return Response(result, status=status.HTTP_201_CREATED)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error uploading VCF file: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def list_vcf_files(self, request):
        """List all uploaded VCF files"""
        if not settings.USE_AWS:
            return Response(
                {'error': 'AWS services not enabled'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        try:
            prefix_date = request.query_params.get('date')
            result = s3_storage.list_vcf_files(prefix_date)
            
            if result['success']:
                return Response(result)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error listing VCF files: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AWSAnnotationJobViewSet(viewsets.ViewSet):
    """ViewSet for managing annotation jobs via AWS SQS"""
    
    @action(detail=False, methods=['post'])
    def create_job(self, request):
        """Create and queue an annotation job"""
        if not settings.USE_AWS:
            return Response(
                {'error': 'AWS services not enabled'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        variant_ids = request.data.get('variant_ids', [])
        sources = request.data.get('sources', [])
        
        if not variant_ids or not sources:
            return Response(
                {'error': 'variant_ids and sources are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            annotation_source = AnnotationSource.objects.filter(name__in=sources).first()
            
            annotation_job = AnnotationJob.objects.create(
                job_id=f"annotation_{len(variant_ids)}_variants",
                status='pending',
                source=annotation_source or AnnotationSource.objects.first(),
                variant_count=len(variant_ids)
            )
            
            result = sqs_handler.send_annotation_job(
                variant_ids,
                sources,
                annotation_job.id
            )
            
            if result['success']:
                return Response({
                    'job_id': annotation_job.id,
                    'message_id': result['message_id'],
                    'variant_count': len(variant_ids),
                    'sources': sources,
                    'status': 'queued'
                }, status=status.HTTP_201_CREATED)
            else:
                annotation_job.delete()
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error creating annotation job: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def list_jobs(self, request):
        """List annotation jobs"""
        try:
            jobs = AnnotationJob.objects.all().order_by('-created_at')
            
            page_size = request.query_params.get('page_size', 20)
            offset = request.query_params.get('offset', 0)
            
            jobs = jobs[int(offset):int(offset) + int(page_size)]
            
            return Response({
                'jobs': [
                    {
                        'id': job.id,
                        'job_id': job.job_id,
                        'status': job.status,
                        'variant_count': job.variant_count,
                        'processed_count': job.processed_count,
                        'created_at': job.created_at.isoformat()
                    }
                    for job in jobs
                ]
            })
        except Exception as e:
            logger.error(f"Error listing annotation jobs: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def job_status(self, request):
        """Get status of a specific annotation job"""
        job_id = request.query_params.get('job_id')
        
        if not job_id:
            return Response(
                {'error': 'job_id parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            job = AnnotationJob.objects.get(id=job_id)
            
            return Response({
                'id': job.id,
                'job_id': job.job_id,
                'status': job.status,
                'variant_count': job.variant_count,
                'processed_count': job.processed_count,
                'failed_count': job.failed_count,
                'created_at': job.created_at.isoformat(),
                'started_at': job.started_at.isoformat() if job.started_at else None,
                'completed_at': job.completed_at.isoformat() if job.completed_at else None
            })
        except AnnotationJob.DoesNotExist:
            return Response(
                {'error': 'Job not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error getting job status: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AWSSyncJobViewSet(viewsets.ViewSet):
    """ViewSet for managing Galaxy sync jobs via AWS SQS"""
    
    @action(detail=False, methods=['post'])
    def create_sync_job(self, request):
        """Create and queue a Galaxy sync job"""
        if not settings.USE_AWS:
            return Response(
                {'error': 'AWS services not enabled'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        galaxy_instance_id = request.data.get('galaxy_instance_id')
        sync_type = request.data.get('sync_type')
        
        if not galaxy_instance_id or not sync_type:
            return Response(
                {'error': 'galaxy_instance_id and sync_type are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            result = sqs_handler.send_sync_job(
                galaxy_instance_id,
                sync_type
            )
            
            if result['success']:
                return Response({
                    'galaxy_instance_id': galaxy_instance_id,
                    'sync_type': sync_type,
                    'message_id': result['message_id'],
                    'status': 'queued'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error creating sync job: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def list_sync_jobs(self, request):
        """List sync jobs"""
        try:
            jobs = GalaxySyncJob.objects.all().order_by('-created_at')
            
            page_size = request.query_params.get('page_size', 20)
            offset = request.query_params.get('offset', 0)
            
            jobs = jobs[int(offset):int(offset) + int(page_size)]
            
            return Response({
                'jobs': [
                    {
                        'id': job.id,
                        'job_type': job.job_type,
                        'status': job.status,
                        'items_processed': job.items_processed,
                        'items_total': job.items_total,
                        'created_at': job.created_at.isoformat()
                    }
                    for job in jobs
                ]
            })
        except Exception as e:
            logger.error(f"Error listing sync jobs: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
def aws_health_check(request):
    """Health check for AWS services"""
    if not settings.USE_AWS:
        return Response({
            'aws_enabled': False,
            'message': 'AWS services not enabled'
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    try:
        health_status = {
            'aws_enabled': True,
            'region': settings.AWS_REGION,
            's3_bucket': settings.AWS_STORAGE_BUCKET_NAME,
            'sqs_queues': settings.SQS_QUEUE_CONFIG if hasattr(settings, 'SQS_QUEUE_CONFIG') else {},
            'status': 'healthy'
        }
        return Response(health_status)
    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
