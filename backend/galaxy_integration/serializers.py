from rest_framework import serializers
from .models import (
    GalaxyInstance, GalaxyHistory, GalaxyDataset, GalaxyWorkflow,
    GalaxySyncJob, GalaxyAPIKey
)


class GalaxyInstanceSerializer(serializers.ModelSerializer):
    """Serializer for GalaxyInstance model"""
    
    class Meta:
        model = GalaxyInstance
        fields = [
            'id', 'name', 'url', 'api_key', 'is_active', 'description',
            'timeout', 'max_retries', 'created_at', 'updated_at', 'last_checked'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_checked']


class GalaxyHistorySerializer(serializers.ModelSerializer):
    """Serializer for GalaxyHistory model"""
    
    galaxy_instance_name = serializers.CharField(source='galaxy_instance.name', read_only=True)
    
    class Meta:
        model = GalaxyHistory
        fields = [
            'id', 'galaxy_instance', 'galaxy_instance_name', 'galaxy_history_id',
            'name', 'status', 'created_at', 'updated_at', 'galaxy_created_at',
            'galaxy_data'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GalaxyDatasetSerializer(serializers.ModelSerializer):
    """Serializer for GalaxyDataset model"""
    
    galaxy_instance_name = serializers.CharField(source='galaxy_instance.name', read_only=True)
    galaxy_history_name = serializers.CharField(source='galaxy_history.name', read_only=True)
    
    class Meta:
        model = GalaxyDataset
        fields = [
            'id', 'galaxy_instance', 'galaxy_instance_name', 'galaxy_history',
            'galaxy_history_name', 'galaxy_dataset_id', 'name', 'file_type',
            'file_size', 'status', 'is_vcf', 'vcf_sample_count', 'vcf_variant_count',
            'is_processed', 'processing_started_at', 'processing_completed_at',
            'local_file_path', 'download_url', 'error_message', 'retry_count',
            'created_at', 'updated_at', 'galaxy_created_at', 'galaxy_data'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GalaxyWorkflowSerializer(serializers.ModelSerializer):
    """Serializer for GalaxyWorkflow model"""
    
    galaxy_instance_name = serializers.CharField(source='galaxy_instance.name', read_only=True)
    
    class Meta:
        model = GalaxyWorkflow
        fields = [
            'id', 'galaxy_instance', 'galaxy_instance_name', 'galaxy_workflow_id',
            'name', 'status', 'description', 'version', 'input_datasets',
            'output_datasets', 'started_at', 'completed_at', 'error_message',
            'created_at', 'updated_at', 'galaxy_data'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class GalaxySyncJobSerializer(serializers.ModelSerializer):
    """Serializer for GalaxySyncJob model"""
    
    galaxy_instance_name = serializers.CharField(source='galaxy_instance.name', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = GalaxySyncJob
        fields = [
            'id', 'galaxy_instance', 'galaxy_instance_name', 'job_type', 'status',
            'items_processed', 'items_total', 'items_failed', 'started_at',
            'completed_at', 'created_at', 'error_message', 'retry_count',
            'max_retries', 'job_config', 'progress_percentage'
        ]
        read_only_fields = ['id', 'created_at', 'progress_percentage']
    
    def get_progress_percentage(self, obj):
        """Calculate progress percentage"""
        if obj.items_total > 0:
            return round((obj.items_processed / obj.items_total) * 100, 2)
        return 0


class GalaxyAPIKeySerializer(serializers.ModelSerializer):
    """Serializer for GalaxyAPIKey model"""
    
    galaxy_instance_name = serializers.CharField(source='galaxy_instance.name', read_only=True)
    
    class Meta:
        model = GalaxyAPIKey
        fields = [
            'id', 'galaxy_instance', 'galaxy_instance_name', 'key_name',
            'api_key', 'is_active', 'created_at', 'expires_at', 'last_used',
            'usage_count', 'last_error'
        ]
        read_only_fields = ['id', 'created_at', 'usage_count']


class GalaxyInstanceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Galaxy instances"""
    
    class Meta:
        model = GalaxyInstance
        fields = [
            'name', 'url', 'api_key', 'is_active', 'description',
            'timeout', 'max_retries'
        ]
    
    def validate_name(self, value):
        """Ensure instance name is unique"""
        if GalaxyInstance.objects.filter(name=value).exists():
            raise serializers.ValidationError("A Galaxy instance with this name already exists.")
        return value


class GalaxyDatasetProcessSerializer(serializers.Serializer):
    """Serializer for processing Galaxy datasets"""
    
    dataset_id = serializers.IntegerField()
    process_vcf = serializers.BooleanField(default=True)
    extract_metadata = serializers.BooleanField(default=True)
    
    def validate_dataset_id(self, value):
        """Validate dataset exists and is VCF"""
        try:
            dataset = GalaxyDataset.objects.get(id=value)
            if dataset.is_vcf and not dataset.is_processed:
                return value
            elif not dataset.is_vcf:
                raise serializers.ValidationError("Dataset is not a VCF file.")
            else:
                raise serializers.ValidationError("Dataset is already processed.")
        except GalaxyDataset.DoesNotExist:
            raise serializers.ValidationError("Dataset not found.")


class GalaxySyncJobCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Galaxy sync jobs"""
    
    class Meta:
        model = GalaxySyncJob
        fields = [
            'galaxy_instance', 'job_type', 'job_config'
        ]
    
    def validate_job_type(self, value):
        """Validate job type"""
        valid_types = ['history', 'dataset', 'workflow']
        if value not in valid_types:
            raise serializers.ValidationError(f"Job type must be one of: {', '.join(valid_types)}")
        return value


class GalaxyStatisticsSerializer(serializers.Serializer):
    """Serializer for Galaxy statistics"""
    
    total_instances = serializers.IntegerField()
    active_instances = serializers.IntegerField()
    total_histories = serializers.IntegerField()
    total_datasets = serializers.IntegerField()
    vcf_datasets = serializers.IntegerField()
    processed_datasets = serializers.IntegerField()
    total_workflows = serializers.IntegerField()
    running_workflows = serializers.IntegerField()
    total_sync_jobs = serializers.IntegerField()
    active_sync_jobs = serializers.IntegerField()
