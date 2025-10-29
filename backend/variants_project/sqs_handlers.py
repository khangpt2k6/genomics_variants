import json
import logging
from datetime import datetime
from variants_project.aws_config import aws_config

logger = logging.getLogger(__name__)


class SQSJobHandler:
    """Handles SQS message processing for background jobs"""
    
    ANNOTATION_QUEUE = 'moffitt-annotation-jobs'
    SYNC_QUEUE = 'moffitt-sync-jobs'
    UPLOAD_QUEUE = 'moffitt-upload-jobs'
    
    @staticmethod
    def send_annotation_job(variant_ids, sources, job_id):
        """Queue annotation job to SQS"""
        try:
            message_body = json.dumps({
                'job_type': 'annotation',
                'job_id': str(job_id),
                'variant_ids': variant_ids,
                'sources': sources,
                'timestamp': datetime.now().isoformat()
            })
            
            success, result = aws_config.send_sqs_message(
                SQSJobHandler.ANNOTATION_QUEUE,
                message_body,
                message_attributes={
                    'job_id': {'StringValue': str(job_id), 'DataType': 'String'},
                    'source_count': {'StringValue': str(len(sources)), 'DataType': 'Number'},
                    'variant_count': {'StringValue': str(len(variant_ids)), 'DataType': 'Number'}
                }
            )
            
            if success:
                logger.info(f"Annotation job queued: {job_id}, Message ID: {result}")
                return {'success': True, 'message_id': result}
            else:
                logger.error(f"Failed to queue annotation job: {result}")
                return {'success': False, 'error': result}
                
        except Exception as e:
            logger.error(f"Error sending annotation job: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def send_sync_job(galaxy_instance_id, job_type, items=None):
        """Queue Galaxy sync job to SQS"""
        try:
            message_body = json.dumps({
                'job_type': 'sync',
                'galaxy_instance_id': galaxy_instance_id,
                'sync_type': job_type,
                'items': items or [],
                'timestamp': datetime.now().isoformat()
            })
            
            success, result = aws_config.send_sqs_message(
                SQSJobHandler.SYNC_QUEUE,
                message_body,
                message_attributes={
                    'galaxy_instance_id': {'StringValue': str(galaxy_instance_id), 'DataType': 'String'},
                    'sync_type': {'StringValue': job_type, 'DataType': 'String'},
                    'item_count': {'StringValue': str(len(items) if items else 0), 'DataType': 'Number'}
                }
            )
            
            if success:
                logger.info(f"Sync job queued: {job_type} for instance {galaxy_instance_id}")
                return {'success': True, 'message_id': result}
            else:
                logger.error(f"Failed to queue sync job: {result}")
                return {'success': False, 'error': result}
                
        except Exception as e:
            logger.error(f"Error sending sync job: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def send_upload_job(s3_key, filename, file_size, metadata=None):
        """Queue file upload job to SQS"""
        try:
            message_body = json.dumps({
                'job_type': 'upload',
                's3_key': s3_key,
                'filename': filename,
                'file_size': file_size,
                'metadata': metadata or {},
                'timestamp': datetime.now().isoformat()
            })
            
            success, result = aws_config.send_sqs_message(
                SQSJobHandler.UPLOAD_QUEUE,
                message_body,
                message_attributes={
                    's3_key': {'StringValue': s3_key, 'DataType': 'String'},
                    'filename': {'StringValue': filename, 'DataType': 'String'},
                    'file_size': {'StringValue': str(file_size), 'DataType': 'Number'}
                }
            )
            
            if success:
                logger.info(f"Upload job queued: {filename} ({file_size} bytes)")
                return {'success': True, 'message_id': result}
            else:
                logger.error(f"Failed to queue upload job: {result}")
                return {'success': False, 'error': result}
                
        except Exception as e:
            logger.error(f"Error sending upload job: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def receive_annotation_jobs(max_messages=5):
        """Receive annotation jobs from SQS"""
        try:
            messages = aws_config.receive_sqs_messages(
                SQSJobHandler.ANNOTATION_QUEUE,
                max_messages=max_messages
            )
            
            jobs = []
            for msg in messages:
                try:
                    body = json.loads(msg['Body'])
                    jobs.append({
                        'message_id': msg['MessageId'],
                        'receipt_handle': msg['ReceiptHandle'],
                        'body': body
                    })
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse message: {msg['MessageId']}")
            
            return {'success': True, 'jobs': jobs}
        except Exception as e:
            logger.error(f"Error receiving annotation jobs: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def receive_sync_jobs(max_messages=5):
        """Receive sync jobs from SQS"""
        try:
            messages = aws_config.receive_sqs_messages(
                SQSJobHandler.SYNC_QUEUE,
                max_messages=max_messages
            )
            
            jobs = []
            for msg in messages:
                try:
                    body = json.loads(msg['Body'])
                    jobs.append({
                        'message_id': msg['MessageId'],
                        'receipt_handle': msg['ReceiptHandle'],
                        'body': body
                    })
                except json.JSONDecodeError:
                    logger.error(f"Failed to parse message: {msg['MessageId']}")
            
            return {'success': True, 'jobs': jobs}
        except Exception as e:
            logger.error(f"Error receiving sync jobs: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def acknowledge_job(queue_name, receipt_handle):
        """Remove job from queue after processing"""
        try:
            success = aws_config.delete_sqs_message(queue_name, receipt_handle)
            if success:
                logger.info(f"Job acknowledged and removed from queue")
                return {'success': True}
            return {'success': False, 'error': 'Failed to acknowledge job'}
        except Exception as e:
            logger.error(f"Error acknowledging job: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def initialize_queues():
        """Create SQS queues if they don't exist"""
        queues = [
            SQSJobHandler.ANNOTATION_QUEUE,
            SQSJobHandler.SYNC_QUEUE,
            SQSJobHandler.UPLOAD_QUEUE
        ]
        
        results = {}
        for queue_name in queues:
            try:
                url = aws_config.create_queue_if_not_exists(queue_name)
                results[queue_name] = {'success': True, 'url': url}
                logger.info(f"Queue ready: {queue_name} - {url}")
            except Exception as e:
                results[queue_name] = {'success': False, 'error': str(e)}
                logger.error(f"Failed to initialize queue {queue_name}: {str(e)}")
        
        return results


sqs_handler = SQSJobHandler()
