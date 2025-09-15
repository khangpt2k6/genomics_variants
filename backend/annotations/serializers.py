from rest_framework import serializers
from .models import (
    AnnotationSource, AnnotationJob, VariantAnnotation, 
    ClinVarAnnotation, COSMICAnnotation, CIViCAnnotation, AnnotationCache
)


class AnnotationSourceSerializer(serializers.ModelSerializer):
    """Serializer for AnnotationSource model"""
    
    class Meta:
        model = AnnotationSource
        fields = [
            'id', 'name', 'version', 'description', 'api_url', 
            'last_updated', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnnotationJobSerializer(serializers.ModelSerializer):
    """Serializer for AnnotationJob model"""
    
    source_name = serializers.CharField(source='source.name', read_only=True)
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = AnnotationJob
        fields = [
            'id', 'job_id', 'status', 'source', 'source_name', 'variant_count',
            'processed_count', 'failed_count', 'started_at', 'completed_at',
            'created_at', 'error_message', 'retry_count', 'max_retries',
            'job_config', 'progress_percentage'
        ]
        read_only_fields = ['id', 'created_at', 'progress_percentage']
    
    def get_progress_percentage(self, obj):
        """Calculate progress percentage"""
        if obj.variant_count > 0:
            return round((obj.processed_count / obj.variant_count) * 100, 2)
        return 0


class VariantAnnotationSerializer(serializers.ModelSerializer):
    """Serializer for VariantAnnotation model"""
    
    variant_id = serializers.IntegerField(source='variant.id', read_only=True)
    variant_display = serializers.CharField(source='variant.__str__', read_only=True)
    source_name = serializers.CharField(source='source.name', read_only=True)
    
    class Meta:
        model = VariantAnnotation
        fields = [
            'id', 'variant_id', 'variant_display', 'source', 'source_name',
            'job', 'annotation_data', 'confidence_score', 'is_successful',
            'error_message', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClinVarAnnotationSerializer(serializers.ModelSerializer):
    """Serializer for ClinVarAnnotation model"""
    
    variant_annotation_id = serializers.IntegerField(source='variant_annotation.id', read_only=True)
    variant_display = serializers.CharField(source='variant_annotation.variant.__str__', read_only=True)
    
    class Meta:
        model = ClinVarAnnotation
        fields = [
            'id', 'variant_annotation_id', 'variant_display', 'clinvar_id',
            'clinical_significance', 'review_status', 'review_date',
            'evidence_level', 'phenotype', 'inheritance_pattern', 'submitter',
            'submission_date', 'clinvar_raw_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class COSMICAnnotationSerializer(serializers.ModelSerializer):
    """Serializer for COSMICAnnotation model"""
    
    variant_annotation_id = serializers.IntegerField(source='variant_annotation.id', read_only=True)
    variant_display = serializers.CharField(source='variant_annotation.variant.__str__', read_only=True)
    
    class Meta:
        model = COSMICAnnotation
        fields = [
            'id', 'variant_annotation_id', 'variant_display', 'cosmic_id',
            'mutation_description', 'mutation_cds', 'mutation_aa',
            'primary_site', 'site_subtype', 'primary_histology',
            'histology_subtype', 'sample_name', 'sample_source',
            'tumour_origin', 'mutation_frequency', 'mutation_count',
            'cosmic_raw_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CIViCAnnotationSerializer(serializers.ModelSerializer):
    """Serializer for CIViCAnnotation model"""
    
    variant_annotation_id = serializers.IntegerField(source='variant_annotation.id', read_only=True)
    variant_display = serializers.CharField(source='variant_annotation.variant.__str__', read_only=True)
    
    class Meta:
        model = CIViCAnnotation
        fields = [
            'id', 'variant_annotation_id', 'variant_display', 'civic_id',
            'evidence_id', 'drug_name', 'response_type', 'evidence_level',
            'evidence_direction', 'cancer_type', 'tissue_type',
            'evidence_type', 'evidence_description', 'clinical_trial_id',
            'civic_raw_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnnotationCacheSerializer(serializers.ModelSerializer):
    """Serializer for AnnotationCache model"""
    
    variant_id = serializers.IntegerField(source='variant.id', read_only=True)
    variant_display = serializers.CharField(source='variant.__str__', read_only=True)
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = AnnotationCache
        fields = [
            'id', 'cache_key', 'variant_id', 'variant_display',
            'cached_data', 'created_at', 'expires_at', 'hit_count', 'is_expired'
        ]
        read_only_fields = ['id', 'created_at', 'hit_count', 'is_expired']
    
    def get_is_expired(self, obj):
        """Check if cache entry is expired"""
        from django.utils import timezone
        return obj.expires_at < timezone.now()


class AnnotationJobCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating annotation jobs"""
    
    class Meta:
        model = AnnotationJob
        fields = [
            'source', 'variant_count', 'job_config'
        ]
    
    def validate_variant_count(self, value):
        """Validate variant count"""
        if value <= 0:
            raise serializers.ValidationError("Variant count must be positive.")
        return value


class AnnotationJobUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating annotation jobs"""
    
    class Meta:
        model = AnnotationJob
        fields = [
            'status', 'processed_count', 'failed_count', 'error_message'
        ]
    
    def validate_status(self, value):
        """Validate status transitions"""
        valid_statuses = ['pending', 'running', 'completed', 'failed', 'cancelled']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of: {', '.join(valid_statuses)}")
        return value


class VariantAnnotationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating variant annotations"""
    
    class Meta:
        model = VariantAnnotation
        fields = [
            'variant', 'source', 'job', 'annotation_data', 'confidence_score',
            'is_successful', 'error_message'
        ]
    
    def validate_confidence_score(self, value):
        """Validate confidence score"""
        if value is not None and (value < 0 or value > 1):
            raise serializers.ValidationError("Confidence score must be between 0 and 1.")
        return value


class AnnotationStatisticsSerializer(serializers.Serializer):
    """Serializer for annotation statistics"""
    
    total_annotations = serializers.IntegerField()
    successful_annotations = serializers.IntegerField()
    failed_annotations = serializers.IntegerField()
    by_source = serializers.DictField()
    average_confidence = serializers.FloatField(allow_null=True)
    success_rate = serializers.SerializerMethodField()
    
    def get_success_rate(self, obj):
        """Calculate success rate"""
        total = obj.get('total_annotations', 0)
        successful = obj.get('successful_annotations', 0)
        if total > 0:
            return round((successful / total) * 100, 2)
        return 0


class AnnotationSourceCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating annotation sources"""
    
    class Meta:
        model = AnnotationSource
        fields = [
            'name', 'version', 'description', 'api_url', 'is_active'
        ]
    
    def validate_name(self, value):
        """Ensure source name is unique"""
        if AnnotationSource.objects.filter(name=value).exists():
            raise serializers.ValidationError("A source with this name already exists.")
        return value


class AnnotationSourceUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating annotation sources"""
    
    class Meta:
        model = AnnotationSource
        fields = [
            'version', 'description', 'api_url', 'last_updated', 'is_active'
        ]
