from django.db import models
from django.contrib.postgres.fields import JSONField


class GalaxyInstance(models.Model):
    """Galaxy server configuration"""
    
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField()
    api_key = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    
    # Connection settings
    timeout = models.PositiveIntegerField(default=30)
    max_retries = models.PositiveIntegerField(default=3)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class GalaxyHistory(models.Model):
    """Galaxy history tracking"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('running', 'Running'),
        ('ok', 'Completed'),
        ('error', 'Error'),
        ('deleted', 'Deleted'),
    ]
    
    galaxy_instance = models.ForeignKey(GalaxyInstance, on_delete=models.CASCADE, related_name='histories')
    galaxy_history_id = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    # History metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    galaxy_created_at = models.DateTimeField(null=True, blank=True)
    
    # Additional Galaxy data
    galaxy_data = JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['galaxy_instance', 'galaxy_history_id']
    
    def __str__(self):
        return f"{self.galaxy_instance.name} - {self.name}"


class GalaxyDataset(models.Model):
    """Galaxy dataset tracking"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('running', 'Running'),
        ('ok', 'Completed'),
        ('error', 'Error'),
        ('deleted', 'Deleted'),
    ]
    
    galaxy_instance = models.ForeignKey(GalaxyInstance, on_delete=models.CASCADE, related_name='datasets')
    galaxy_history = models.ForeignKey(GalaxyHistory, on_delete=models.CASCADE, related_name='datasets')
    galaxy_dataset_id = models.CharField(max_length=100, db_index=True)
    
    # Dataset information
    name = models.CharField(max_length=200)
    file_type = models.CharField(max_length=50)
    file_size = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    # VCF specific fields
    is_vcf = models.BooleanField(default=False)
    vcf_sample_count = models.PositiveIntegerField(null=True, blank=True)
    vcf_variant_count = models.PositiveIntegerField(null=True, blank=True)
    
    # Processing status
    is_processed = models.BooleanField(default=False)
    processing_started_at = models.DateTimeField(null=True, blank=True)
    processing_completed_at = models.DateTimeField(null=True, blank=True)
    
    # File paths
    local_file_path = models.CharField(max_length=500, blank=True)
    download_url = models.URLField(blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    galaxy_created_at = models.DateTimeField(null=True, blank=True)
    
    # Additional Galaxy data
    galaxy_data = JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['galaxy_instance', 'galaxy_dataset_id']
        indexes = [
            models.Index(fields=['is_vcf', 'is_processed']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.file_type})"


class GalaxyWorkflow(models.Model):
    """Galaxy workflow tracking"""
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('error', 'Error'),
        ('cancelled', 'Cancelled'),
    ]
    
    galaxy_instance = models.ForeignKey(GalaxyInstance, on_delete=models.CASCADE, related_name='workflows')
    galaxy_workflow_id = models.CharField(max_length=100, db_index=True)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    # Workflow details
    description = models.TextField(blank=True)
    version = models.CharField(max_length=20, blank=True)
    
    # Input/Output datasets
    input_datasets = models.ManyToManyField(GalaxyDataset, related_name='input_workflows', blank=True)
    output_datasets = models.ManyToManyField(GalaxyDataset, related_name='output_workflows', blank=True)
    
    # Execution details
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Error handling
    error_message = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional Galaxy data
    galaxy_data = JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['galaxy_instance', 'galaxy_workflow_id']
    
    def __str__(self):
        return f"{self.name} - {self.status}"


class GalaxySyncJob(models.Model):
    """Galaxy synchronization job tracking"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    galaxy_instance = models.ForeignKey(GalaxyInstance, on_delete=models.CASCADE, related_name='sync_jobs')
    job_type = models.CharField(max_length=50)  # 'history', 'dataset', 'workflow'
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Job details
    items_processed = models.PositiveIntegerField(default=0)
    items_total = models.PositiveIntegerField(default=0)
    items_failed = models.PositiveIntegerField(default=0)
    
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
        return f"Sync Job {self.id} - {self.job_type} - {self.status}"


class GalaxyAPIKey(models.Model):
    """Galaxy API key management"""
    
    galaxy_instance = models.ForeignKey(GalaxyInstance, on_delete=models.CASCADE, related_name='api_keys')
    key_name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    
    # Key metadata
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    # Usage tracking
    usage_count = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['galaxy_instance', 'key_name']
    
    def __str__(self):
        return f"{self.galaxy_instance.name} - {self.key_name}"