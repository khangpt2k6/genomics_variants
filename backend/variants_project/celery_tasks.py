import os
import logging
from celery import Celery, shared_task
from django.conf import settings
from .sqs_messaging import SQSMessageHandler, QueueMessage

logger = logging.getLogger(__name__)

app = Celery('moffitt_variants')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@shared_task(bind=True, max_retries=3)
def process_annotation_job(self, message_dict):
    """
    Process variant annotation job from SQS
    
    Args:
        message_dict: Dictionary containing job details
    """
    try:
        from annotations.models import AnnotationJob, VariantAnnotation
        from variants.models import Variant
        
        variant_id = message_dict.get('variant_id')
        annotation_source = message_dict.get('annotation_source')
        job_config = message_dict.get('job_config', {})
        
        if not variant_id or not annotation_source:
            logger.error("Missing variant_id or annotation_source")
            return False
        
        variant = Variant.objects.get(id=variant_id)
        
        job = AnnotationJob.objects.create(
            job_id=f"celery-{self.request.id}",
            status='running',
            source_id=job_config.get('source_id'),
            variant_count=1
        )
        
        logger.info(f"Processing annotation for variant {variant_id} from {annotation_source}")
        
        job.status = 'completed'
        job.processed_count = 1
        job.save()
        
        return True
        
    except Exception as exc:
        logger.error(f"Error processing annotation job: {str(exc)}")
        self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def process_sync_job(self, message_dict):
    """
    Process Galaxy synchronization job from SQS
    
    Args:
        message_dict: Dictionary containing sync job details
    """
    try:
        from galaxy_integration.models import GalaxySyncJob, GalaxyInstance
        
        galaxy_instance_id = message_dict.get('galaxy_instance_id')
        job_type = message_dict.get('job_type')
        job_config = message_dict.get('job_config', {})
        
        if not galaxy_instance_id or not job_type:
            logger.error("Missing galaxy_instance_id or job_type")
            return False
        
        galaxy_instance = GalaxyInstance.objects.get(id=galaxy_instance_id)
        
        sync_job = GalaxySyncJob.objects.create(
            galaxy_instance=galaxy_instance,
            job_type=job_type,
            status='running'
        )
        
        logger.info(f"Processing {job_type} sync for Galaxy instance {galaxy_instance_id}")
        
        sync_job.status = 'completed'
        sync_job.save()
        
        return True
        
    except Exception as exc:
        logger.error(f"Error processing sync job: {str(exc)}")
        self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def process_vcf_upload(self, file_key, file_name, metadata):
    """
    Process VCF file upload from S3
    
    Args:
        file_key: S3 object key
        file_name: Original file name
        metadata: File metadata
    """
    try:
        from variants.models import Variant
        from variants_project.aws_config import aws_config
        import vcf
        from io import StringIO
        
        logger.info(f"Processing VCF upload: {file_name}")
        
        try:
            vcf_content = aws_config.download_from_s3(file_key)
            
            if not vcf_content:
                logger.error(f"Failed to download VCF from S3: {file_key}")
                return False
            
            vcf_file = StringIO(vcf_content.decode('utf-8'))
            vcf_reader = vcf.Reader(vcf_file)
            
            variant_count = 0
            for record in vcf_reader:
                variant, created = Variant.objects.update_or_create(
                    variant_id=record.ID,
                    defaults={
                        'chromosome': record.CHROM,
                        'position': record.POS,
                        'reference_allele': record.REF,
                        'alternate_allele': str(record.ALT[0]) if record.ALT else '',
                        'quality_score': record.QUAL,
                        'filter_status': ','.join(record.FILTER) if record.FILTER else 'PASS',
                        'vcf_data': {
                            'info': dict(record.INFO) if record.INFO else {},
                            'format': record.FORMAT if record.FORMAT else ''
                        }
                    }
                )
                variant_count += 1
            
            logger.info(f"Successfully processed {variant_count} variants from {file_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error parsing VCF file: {str(e)}")
            return False
            
    except Exception as exc:
        logger.error(f"Error processing VCF upload: {str(exc)}")
        self.retry(exc=exc, countdown=60)


@shared_task
def consume_annotation_queue():
    """
    Consume messages from annotation queue
    This task can be scheduled to run periodically
    """
    try:
        messages = SQSMessageHandler.receive_messages(
            'moffitt-annotation-jobs',
            max_messages=10
        )
        
        for message in messages:
            try:
                queue_msg = QueueMessage(message)
                process_annotation_job.delay(queue_msg.to_dict())
                SQSMessageHandler.delete_message(
                    'moffitt-annotation-jobs',
                    queue_msg.receipt_handle
                )
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
        
        return len(messages)
        
    except Exception as e:
        logger.error(f"Error consuming annotation queue: {str(e)}")
        return 0


@shared_task
def consume_sync_queue():
    """
    Consume messages from sync queue
    This task can be scheduled to run periodically
    """
    try:
        messages = SQSMessageHandler.receive_messages(
            'moffitt-sync-jobs',
            max_messages=10
        )
        
        for message in messages:
            try:
                queue_msg = QueueMessage(message)
                process_sync_job.delay(queue_msg.to_dict())
                SQSMessageHandler.delete_message(
                    'moffitt-sync-jobs',
                    queue_msg.receipt_handle
                )
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
        
        return len(messages)
        
    except Exception as e:
        logger.error(f"Error consuming sync queue: {str(e)}")
        return 0


@shared_task
def consume_upload_queue():
    """
    Consume messages from upload queue
    This task can be scheduled to run periodically
    """
    try:
        messages = SQSMessageHandler.receive_messages(
            'moffitt-upload-jobs',
            max_messages=10
        )
        
        for message in messages:
            try:
                body = eval(message['Body'])
                process_vcf_upload.delay(
                    body['file_key'],
                    body['file_name'],
                    body['metadata']
                )
                SQSMessageHandler.delete_message(
                    'moffitt-upload-jobs',
                    message['ReceiptHandle']
                )
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
        
        return len(messages)
        
    except Exception as e:
        logger.error(f"Error consuming upload queue: {str(e)}")
        return 0
