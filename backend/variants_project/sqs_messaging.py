import json
import logging
from typing import Dict, Any, Optional, List
from .aws_config import aws_config

logger = logging.getLogger(__name__)


class SQSMessageHandler:
    """Handle SQS messaging for async job processing"""
    
    @staticmethod
    def send_annotation_job(variant_id: int, annotation_source: str, job_config: Dict[str, Any]) -> tuple:
        """
        Send annotation job to SQS queue
        
        Args:
            variant_id: ID of the variant to annotate
            annotation_source: Source of annotation (ClinVar, COSMIC, CIViC)
            job_config: Additional job configuration
            
        Returns:
            (success, message_id or error_message)
        """
        try:
            message_body = {
                'variant_id': variant_id,
                'annotation_source': annotation_source,
                'job_config': job_config,
                'action': 'annotate'
            }
            
            return aws_config.send_sqs_message(
                aws_config.sqs_annotation_queue,
                json.dumps(message_body),
                message_attributes={
                    'VariantId': {
                        'StringValue': str(variant_id),
                        'DataType': 'String'
                    },
                    'Source': {
                        'StringValue': annotation_source,
                        'DataType': 'String'
                    }
                }
            )
        except Exception as e:
            logger.error(f"Failed to send annotation job: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def send_sync_job(galaxy_instance_id: int, job_type: str, job_config: Dict[str, Any]) -> tuple:
        """
        Send Galaxy sync job to SQS queue
        
        Args:
            galaxy_instance_id: ID of the Galaxy instance
            job_type: Type of sync job (history, dataset, workflow)
            job_config: Additional job configuration
            
        Returns:
            (success, message_id or error_message)
        """
        try:
            message_body = {
                'galaxy_instance_id': galaxy_instance_id,
                'job_type': job_type,
                'job_config': job_config,
                'action': 'sync'
            }
            
            return aws_config.send_sqs_message(
                aws_config.sqs_sync_queue,
                json.dumps(message_body),
                message_attributes={
                    'GalaxyInstanceId': {
                        'StringValue': str(galaxy_instance_id),
                        'DataType': 'String'
                    },
                    'JobType': {
                        'StringValue': job_type,
                        'DataType': 'String'
                    }
                }
            )
        except Exception as e:
            logger.error(f"Failed to send sync job: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def send_vcf_upload_job(file_key: str, file_name: str, metadata: Dict[str, Any]) -> tuple:
        """
        Send VCF file upload job to SQS queue
        
        Args:
            file_key: S3 object key
            file_name: Original file name
            metadata: File metadata
            
        Returns:
            (success, message_id or error_message)
        """
        try:
            message_body = {
                'file_key': file_key,
                'file_name': file_name,
                'metadata': metadata,
                'action': 'process_vcf'
            }
            
            return aws_config.send_sqs_message(
                'moffitt-upload-jobs',
                json.dumps(message_body),
                message_attributes={
                    'FileName': {
                        'StringValue': file_name,
                        'DataType': 'String'
                    },
                    'FileKey': {
                        'StringValue': file_key,
                        'DataType': 'String'
                    }
                }
            )
        except Exception as e:
            logger.error(f"Failed to send upload job: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def receive_messages(queue_name: str, max_messages: int = 10) -> List[Dict[str, Any]]:
        """
        Receive messages from SQS queue
        
        Args:
            queue_name: Name of the queue
            max_messages: Maximum number of messages to receive
            
        Returns:
            List of messages
        """
        try:
            messages = aws_config.receive_sqs_messages(queue_name, max_messages)
            return messages
        except Exception as e:
            logger.error(f"Failed to receive messages: {str(e)}")
            return []
    
    @staticmethod
    def delete_message(queue_name: str, receipt_handle: str) -> bool:
        """
        Delete message from SQS queue
        
        Args:
            queue_name: Name of the queue
            receipt_handle: Message receipt handle
            
        Returns:
            Success status
        """
        try:
            return aws_config.delete_sqs_message(queue_name, receipt_handle)
        except Exception as e:
            logger.error(f"Failed to delete message: {str(e)}")
            return False
    
    @staticmethod
    def create_queues() -> Dict[str, bool]:
        """
        Create SQS queues if they don't exist
        
        Returns:
            Dictionary with queue creation status
        """
        queues = {
            'annotation': aws_config.sqs_annotation_queue,
            'sync': aws_config.sqs_sync_queue,
            'upload': 'moffitt-upload-jobs'
        }
        
        results = {}
        for queue_type, queue_name in queues.items():
            try:
                aws_config.create_queue_if_not_exists(queue_name)
                results[queue_type] = True
                logger.info(f"Queue {queue_name} created or verified")
            except Exception as e:
                logger.error(f"Failed to create queue {queue_name}: {str(e)}")
                results[queue_type] = False
        
        return results


class QueueMessage:
    """Helper class to parse SQS message"""
    
    def __init__(self, message: Dict[str, Any]):
        self.message = message
        self.message_id = message.get('MessageId')
        self.receipt_handle = message.get('ReceiptHandle')
        self.body = json.loads(message.get('Body', '{}'))
        self.attributes = message.get('MessageAttributes', {})
    
    def get_variant_id(self) -> Optional[int]:
        """Get variant ID from message"""
        return self.body.get('variant_id')
    
    def get_annotation_source(self) -> Optional[str]:
        """Get annotation source from message"""
        return self.body.get('annotation_source')
    
    def get_action(self) -> Optional[str]:
        """Get action from message"""
        return self.body.get('action')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary"""
        return self.body
