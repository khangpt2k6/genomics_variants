import os
import boto3
from botocore.config import Config


class AWSConfig:
    """AWS configuration and client management"""
    
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        self.s3_bucket = os.getenv('AWS_S3_BUCKET_NAME', 'moffitt-variants')
        self.sqs_queue_url = os.getenv('AWS_SQS_QUEUE_URL')
        self.sqs_annotation_queue = os.getenv('AWS_SQS_ANNOTATION_QUEUE', 'moffitt-annotation-jobs')
        self.sqs_sync_queue = os.getenv('AWS_SQS_SYNC_QUEUE', 'moffitt-sync-jobs')
        
        self.rds_db_name = os.getenv('RDS_DB_NAME', 'moffitt_variants')
        self.rds_db_user = os.getenv('RDS_DB_USER', 'moffitt_user')
        self.rds_db_password = os.getenv('RDS_DB_PASSWORD')
        self.rds_db_host = os.getenv('RDS_DB_HOST', 'localhost')
        self.rds_db_port = os.getenv('RDS_DB_PORT', '5432')
        
        self._s3_client = None
        self._sqs_client = None
        self._rds_client = None
    
    @property
    def s3_client(self):
        """Get or create S3 client"""
        if self._s3_client is None:
            config = Config(max_pool_connections=50)
            self._s3_client = boto3.client(
                's3',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                config=config
            )
        return self._s3_client
    
    @property
    def sqs_client(self):
        """Get or create SQS client"""
        if self._sqs_client is None:
            self._sqs_client = boto3.client(
                'sqs',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key
            )
        return self._sqs_client
    
    @property
    def rds_client(self):
        """Get or create RDS client"""
        if self._rds_client is None:
            self._rds_client = boto3.client(
                'rds',
                region_name=self.region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key
            )
        return self._rds_client
    
    def get_s3_url(self, key):
        """Generate S3 object URL"""
        return f"https://{self.s3_bucket}.s3.{self.region}.amazonaws.com/{key}"
    
    def upload_to_s3(self, file_obj, key, metadata=None):
        """Upload file to S3"""
        try:
            extra_args = {}
            if metadata:
                extra_args['Metadata'] = metadata
            
            self.s3_client.upload_fileobj(
                file_obj,
                self.s3_bucket,
                key,
                ExtraArgs=extra_args
            )
            return True, self.get_s3_url(key)
        except Exception as e:
            return False, str(e)
    
    def download_from_s3(self, key):
        """Download file from S3"""
        try:
            response = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=key
            )
            return response['Body'].read()
        except Exception as e:
            return None
    
    def delete_from_s3(self, key):
        """Delete file from S3"""
        try:
            self.s3_client.delete_object(
                Bucket=self.s3_bucket,
                Key=key
            )
            return True
        except Exception as e:
            return False
    
    def send_sqs_message(self, queue_name, message_body, message_attributes=None):
        """Send message to SQS queue"""
        try:
            queue_url = self.get_queue_url(queue_name)
            
            params = {
                'QueueUrl': queue_url,
                'MessageBody': message_body
            }
            
            if message_attributes:
                params['MessageAttributes'] = message_attributes
            
            response = self.sqs_client.send_message(**params)
            return True, response['MessageId']
        except Exception as e:
            return False, str(e)
    
    def receive_sqs_messages(self, queue_name, max_messages=10, wait_time=20):
        """Receive messages from SQS queue"""
        try:
            queue_url = self.get_queue_url(queue_name)
            
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,
                MessageAttributeNames=['All']
            )
            
            return response.get('Messages', [])
        except Exception as e:
            return []
    
    def delete_sqs_message(self, queue_name, receipt_handle):
        """Delete message from SQS queue"""
        try:
            queue_url = self.get_queue_url(queue_name)
            
            self.sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            return True
        except Exception as e:
            return False
    
    def get_queue_url(self, queue_name):
        """Get SQS queue URL"""
        try:
            response = self.sqs_client.get_queue_url(QueueName=queue_name)
            return response['QueueUrl']
        except Exception as e:
            raise Exception(f"Failed to get queue URL for {queue_name}: {str(e)}")
    
    def create_queue_if_not_exists(self, queue_name):
        """Create SQS queue if it doesn't exist"""
        try:
            response = self.sqs_client.create_queue(
                QueueName=queue_name,
                Attributes={
                    'VisibilityTimeout': '300',
                    'MessageRetentionPeriod': '1209600'
                }
            )
            return response['QueueUrl']
        except self.sqs_client.exceptions.QueueNameExists:
            return self.get_queue_url(queue_name)
        except Exception as e:
            raise Exception(f"Failed to create queue {queue_name}: {str(e)}")


aws_config = AWSConfig()
