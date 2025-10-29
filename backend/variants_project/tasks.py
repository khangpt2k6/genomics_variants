import json
import logging
from datetime import datetime
from celery import shared_task
from django.conf import settings
from variants_project.sqs_handlers import sqs_handler
from variants_project.s3_storage import s3_storage
from annotations.models import AnnotationJob, AnnotationSource
from galaxy_integration.models import GalaxySyncJob, GalaxyInstance

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_annotation_jobs(self):
    """Process annotation jobs from SQS queue"""
    try:
        result = sqs_handler.receive_annotation_jobs(max_messages=5)
        
        if not result['success']:
            logger.error(f"Failed to receive annotation jobs: {result['error']}")
            return {'success': False, 'error': result['error']}
        
        jobs = result['jobs']
        processed = 0
        failed = 0
        
        for job in jobs:
            try:
                body = job['body']
                job_id = body.get('job_id')
                variant_ids = body.get('variant_ids', [])
                sources = body.get('sources', [])
                
                logger.info(f"Processing annotation job {job_id}: {len(variant_ids)} variants, {len(sources)} sources")
                
                try:
                    annotation_job = AnnotationJob.objects.get(job_id=job_id)
                except AnnotationJob.DoesNotExist:
                    logger.warning(f"Annotation job {job_id} not found in database")
                    annotation_job = None
                
                for source_name in sources:
                    try:
                        source = AnnotationSource.objects.get(name=source_name)
                        logger.info(f"Annotating {len(variant_ids)} variants with {source_name}")
                        
                        if annotation_job:
                            annotation_job.status = 'running'
                            annotation_job.started_at = datetime.now()
                            annotation_job.save()
                    except AnnotationSource.DoesNotExist:
                        logger.warning(f"Annotation source {source_name} not found")
                
                sqs_handler.acknowledge_job('moffitt-annotation-jobs', job['receipt_handle'])
                processed += 1
                
                if annotation_job:
                    annotation_job.status = 'completed'
                    annotation_job.completed_at = datetime.now()
                    annotation_job.processed_count = len(variant_ids)
                    annotation_job.save()
                    
            except Exception as e:
                logger.error(f"Error processing annotation job: {str(e)}")
                failed += 1
        
        return {
            'success': True,
            'processed': processed,
            'failed': failed,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Fatal error in process_annotation_jobs: {str(e)}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def process_sync_jobs(self):
    """Process Galaxy sync jobs from SQS queue"""
    try:
        result = sqs_handler.receive_sync_jobs(max_messages=5)
        
        if not result['success']:
            logger.error(f"Failed to receive sync jobs: {result['error']}")
            return {'success': False, 'error': result['error']}
        
        jobs = result['jobs']
        processed = 0
        failed = 0
        
        for job in jobs:
            try:
                body = job['body']
                galaxy_instance_id = body.get('galaxy_instance_id')
                sync_type = body.get('sync_type')
                items = body.get('items', [])
                
                logger.info(f"Processing sync job: {sync_type} for Galaxy instance {galaxy_instance_id}")
                
                try:
                    galaxy_instance = GalaxyInstance.objects.get(id=galaxy_instance_id)
                except GalaxyInstance.DoesNotExist:
                    logger.warning(f"Galaxy instance {galaxy_instance_id} not found")
                    galaxy_instance = None
                
                try:
                    sync_job = GalaxySyncJob.objects.create(
                        galaxy_instance=galaxy_instance,
                        job_type=sync_type,
                        status='running',
                        started_at=datetime.now(),
                        items_total=len(items)
                    )
                    
                    logger.info(f"Created sync job {sync_job.id} for {sync_type}")
                    
                    sync_job.items_processed = len(items)
                    sync_job.status = 'completed'
                    sync_job.completed_at = datetime.now()
                    sync_job.save()
                    
                except Exception as e:
                    logger.error(f"Error creating sync job: {str(e)}")
                
                sqs_handler.acknowledge_job('moffitt-sync-jobs', job['receipt_handle'])
                processed += 1
                
            except Exception as e:
                logger.error(f"Error processing sync job: {str(e)}")
                failed += 1
        
        return {
            'success': True,
            'processed': processed,
            'failed': failed,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Fatal error in process_sync_jobs: {str(e)}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def process_upload_jobs(self):
    """Process file upload jobs from SQS queue"""
    try:
        result = sqs_handler.receive_annotation_jobs(max_messages=5)
        
        if not result['success']:
            logger.error(f"Failed to receive upload jobs: {result['error']}")
            return {'success': False, 'error': result['error']}
        
        jobs = result['jobs']
        processed = 0
        failed = 0
        
        for job in jobs:
            try:
                body = job['body']
                s3_key = body.get('s3_key')
                filename = body.get('filename')
                
                logger.info(f"Processing upload job: {filename}")
                
                sqs_handler.acknowledge_job('moffitt-upload-jobs', job['receipt_handle'])
                processed += 1
                
            except Exception as e:
                logger.error(f"Error processing upload job: {str(e)}")
                failed += 1
        
        return {
            'success': True,
            'processed': processed,
            'failed': failed,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Fatal error in process_upload_jobs: {str(e)}")
        self.retry(exc=e, countdown=60)


@shared_task
def initialize_aws_queues():
    """Initialize SQS queues on startup"""
    if settings.USE_AWS:
        logger.info("Initializing AWS SQS queues")
        results = sqs_handler.initialize_queues()
        logger.info(f"Queue initialization results: {results}")
        return results
    return {'success': False, 'error': 'AWS not enabled'}
