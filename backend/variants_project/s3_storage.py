import os
import json
from datetime import datetime
from io import BytesIO
import logging
from variants_project.aws_config import aws_config

logger = logging.getLogger(__name__)


class S3VCFStorage:
    """S3 storage handler for VCF files and genomic data"""
    
    VCF_PREFIX = 'vcf-files'
    ANNOTATION_PREFIX = 'annotations'
    RESULTS_PREFIX = 'results'
    
    @staticmethod
    def upload_vcf_file(file_obj, filename, metadata=None):
        """Upload VCF file to S3"""
        try:
            key = f"{S3VCFStorage.VCF_PREFIX}/{datetime.now().strftime('%Y/%m/%d')}/{filename}"
            
            upload_metadata = {
                'upload_timestamp': datetime.now().isoformat(),
                'original_filename': filename,
            }
            
            if metadata:
                upload_metadata.update(metadata)
            
            success, result = aws_config.upload_to_s3(
                file_obj,
                key,
                metadata=upload_metadata
            )
            
            if success:
                logger.info(f"VCF file uploaded: {key}")
                return {
                    'success': True,
                    'key': key,
                    'url': result,
                    'filename': filename,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                logger.error(f"Failed to upload VCF: {result}")
                return {'success': False, 'error': result}
                
        except Exception as e:
            logger.error(f"Error uploading VCF file: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def download_vcf_file(s3_key):
        """Download VCF file from S3"""
        try:
            data = aws_config.download_from_s3(s3_key)
            if data:
                return {'success': True, 'data': data}
            return {'success': False, 'error': 'File not found'}
        except Exception as e:
            logger.error(f"Error downloading VCF file: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def upload_annotation_result(data, job_id, annotation_source):
        """Upload annotation results to S3"""
        try:
            key = f"{S3VCFStorage.ANNOTATION_PREFIX}/{annotation_source}/{datetime.now().strftime('%Y/%m/%d')}/job_{job_id}.json"
            
            file_obj = BytesIO(json.dumps(data).encode('utf-8'))
            
            success, result = aws_config.upload_to_s3(
                file_obj,
                key,
                metadata={
                    'job_id': str(job_id),
                    'annotation_source': annotation_source,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            if success:
                logger.info(f"Annotation result uploaded: {key}")
                return {'success': True, 'key': key, 'url': result}
            else:
                logger.error(f"Failed to upload annotation result: {result}")
                return {'success': False, 'error': result}
                
        except Exception as e:
            logger.error(f"Error uploading annotation result: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def upload_processing_result(data, variant_count, processing_type):
        """Upload variant processing results to S3"""
        try:
            key = f"{S3VCFStorage.RESULTS_PREFIX}/{processing_type}/{datetime.now().strftime('%Y/%m/%d')}/results_{variant_count}_variants.json"
            
            file_obj = BytesIO(json.dumps(data).encode('utf-8'))
            
            success, result = aws_config.upload_to_s3(
                file_obj,
                key,
                metadata={
                    'variant_count': str(variant_count),
                    'processing_type': processing_type,
                    'timestamp': datetime.now().isoformat()
                }
            )
            
            if success:
                logger.info(f"Processing result uploaded: {key}")
                return {'success': True, 'key': key, 'url': result}
            else:
                logger.error(f"Failed to upload processing result: {result}")
                return {'success': False, 'error': result}
                
        except Exception as e:
            logger.error(f"Error uploading processing result: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def list_vcf_files(prefix_date=None):
        """List VCF files in S3"""
        try:
            if prefix_date:
                prefix = f"{S3VCFStorage.VCF_PREFIX}/{prefix_date}"
            else:
                prefix = S3VCFStorage.VCF_PREFIX
            
            response = aws_config.s3_client.list_objects_v2(
                Bucket=aws_config.s3_bucket,
                Prefix=prefix
            )
            
            files = []
            if 'Contents' in response:
                for obj in response['Contents']:
                    files.append({
                        'key': obj['Key'],
                        'size': obj['Size'],
                        'last_modified': obj['LastModified'].isoformat(),
                        'url': aws_config.get_s3_url(obj['Key'])
                    })
            
            return {'success': True, 'files': files}
        except Exception as e:
            logger.error(f"Error listing VCF files: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_file(s3_key):
        """Delete file from S3"""
        try:
            success = aws_config.delete_from_s3(s3_key)
            if success:
                logger.info(f"File deleted: {s3_key}")
                return {'success': True}
            return {'success': False, 'error': 'Failed to delete file'}
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return {'success': False, 'error': str(e)}


s3_storage = S3VCFStorage()
