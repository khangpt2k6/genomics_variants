from django.db import models
from django.contrib.postgres.fields import JSONField
from variants.models import Variant


class AnnotationSource(models.Model):
    """Represents different annotation sources (ClinVar, COSMIC, CIViC, etc.)"""
    
    name = models.CharField(max_length=100, unique=True)
    version = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    api_url = models.URLField(blank=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} v{self.version}"


class AnnotationJob(models.Model):
    """Tracks annotation jobs for variants"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    job_id = models.CharField(max_length=100, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Job details
    source = models.ForeignKey(AnnotationSource, on_delete=models.CASCADE)
    variant_count = models.PositiveIntegerField()
    processed_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    max_retries = models.PositiveIntegerField(default=3)
    
    # Job configuration
    job_config = JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Annotation Job {self.job_id} - {self.status}"


class VariantAnnotation(models.Model):
    """Individual variant annotations from various sources"""
    
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='annotations')
    source = models.ForeignKey(AnnotationSource, on_delete=models.CASCADE)
    job = models.ForeignKey(AnnotationJob, on_delete=models.CASCADE, null=True, blank=True)
    
    # Annotation data
    annotation_data = JSONField(default=dict)
    confidence_score = models.FloatField(null=True, blank=True)
    
    # Status
    is_successful = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['variant', 'source']
        indexes = [
            models.Index(fields=['variant', 'source']),
            models.Index(fields=['is_successful']),
        ]
    
    def __str__(self):
        return f"{self.variant} - {self.source}"


class ClinVarAnnotation(models.Model):
    """Detailed ClinVar annotation data"""
    
    variant_annotation = models.OneToOneField(VariantAnnotation, on_delete=models.CASCADE, related_name='clinvar_data')
    
    # ClinVar specific fields
    clinvar_id = models.CharField(max_length=50, db_index=True)
    clinical_significance = models.CharField(max_length=50)
    review_status = models.CharField(max_length=50)
    review_date = models.DateField(null=True, blank=True)
    
    # Evidence details
    evidence_level = models.CharField(max_length=50, null=True, blank=True)
    phenotype = models.TextField(blank=True)
    inheritance_pattern = models.CharField(max_length=50, blank=True)
    
    # Submission details
    submitter = models.CharField(max_length=200, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    
    # Additional ClinVar data
    clinvar_raw_data = JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-review_date', 'clinical_significance']
    
    def __str__(self):
        return f"ClinVar {self.clinvar_id} - {self.clinical_significance}"


class COSMICAnnotation(models.Model):
    """Detailed COSMIC annotation data"""
    
    variant_annotation = models.OneToOneField(VariantAnnotation, on_delete=models.CASCADE, related_name='cosmic_data')
    
    # COSMIC specific fields
    cosmic_id = models.CharField(max_length=50, unique=True, db_index=True)
    mutation_description = models.TextField(blank=True)
    mutation_cds = models.CharField(max_length=200, blank=True)
    mutation_aa = models.CharField(max_length=200, blank=True)
    
    # Cancer information
    primary_site = models.CharField(max_length=100, blank=True)
    site_subtype = models.CharField(max_length=100, blank=True)
    primary_histology = models.CharField(max_length=100, blank=True)
    histology_subtype = models.CharField(max_length=100, blank=True)
    
    # Sample information
    sample_name = models.CharField(max_length=100, blank=True)
    sample_source = models.CharField(max_length=100, blank=True)
    tumour_origin = models.CharField(max_length=50, blank=True)
    
    # Frequency data
    mutation_frequency = models.FloatField(null=True, blank=True)
    mutation_count = models.PositiveIntegerField(null=True, blank=True)
    
    # Additional COSMIC data
    cosmic_raw_data = JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['cosmic_id']
    
    def __str__(self):
        return f"COSMIC {self.cosmic_id} - {self.primary_site}"


class CIViCAnnotation(models.Model):
    """Detailed CIViC annotation data"""
    
    variant_annotation = models.OneToOneField(VariantAnnotation, on_delete=models.CASCADE, related_name='civic_data')
    
    # CIViC specific fields
    civic_id = models.CharField(max_length=50, db_index=True)
    evidence_id = models.CharField(max_length=50, blank=True)
    
    # Drug information
    drug_name = models.CharField(max_length=200)
    response_type = models.CharField(max_length=50)  # sensitivity, resistance, etc.
    evidence_level = models.CharField(max_length=20)  # A, B, C, D
    evidence_direction = models.CharField(max_length=20)  # supports, does not support
    
    # Clinical context
    cancer_type = models.CharField(max_length=200, blank=True)
    tissue_type = models.CharField(max_length=100, blank=True)
    
    # Evidence details
    evidence_type = models.CharField(max_length=50, blank=True)
    evidence_description = models.TextField(blank=True)
    clinical_trial_id = models.CharField(max_length=50, blank=True)
    
    # Additional CIViC data
    civic_raw_data = JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['drug_name', 'evidence_level']
    
    def __str__(self):
        return f"CIViC {self.civic_id} - {self.drug_name}"


class AnnotationCache(models.Model):
    """Cache for frequently accessed annotation data"""
    
    cache_key = models.CharField(max_length=200, unique=True, db_index=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='cached_annotations')
    
    # Cached data
    cached_data = JSONField(default=dict)
    
    # Cache metadata
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    hit_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['cache_key']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"Cache {self.cache_key} - {self.variant}"