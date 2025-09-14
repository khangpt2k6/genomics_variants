from django.contrib import admin
from .models import (
    GalaxyInstance, GalaxyHistory, GalaxyDataset, GalaxyWorkflow,
    GalaxySyncJob, GalaxyAPIKey
)


@admin.register(GalaxyInstance)
class GalaxyInstanceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'url', 'is_active', 'last_checked', 'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'url', 'description']
    readonly_fields = ['created_at', 'updated_at', 'last_checked']


@admin.register(GalaxyHistory)
class GalaxyHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'galaxy_instance', 'status', 'galaxy_history_id',
        'created_at', 'galaxy_created_at'
    ]
    list_filter = [
        'status', 'galaxy_instance', 'created_at'
    ]
    search_fields = [
        'name', 'galaxy_history_id', 'galaxy_instance__name'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GalaxyDataset)
class GalaxyDatasetAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'galaxy_instance', 'file_type', 'status', 'is_vcf',
        'is_processed', 'file_size', 'created_at'
    ]
    list_filter = [
        'file_type', 'status', 'is_vcf', 'is_processed', 'galaxy_instance', 'created_at'
    ]
    search_fields = [
        'name', 'galaxy_dataset_id', 'galaxy_instance__name'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GalaxyWorkflow)
class GalaxyWorkflowAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'galaxy_instance', 'status', 'version',
        'started_at', 'completed_at', 'created_at'
    ]
    list_filter = [
        'status', 'galaxy_instance', 'started_at', 'completed_at'
    ]
    search_fields = [
        'name', 'galaxy_workflow_id', 'galaxy_instance__name', 'description'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(GalaxySyncJob)
class GalaxySyncJobAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'galaxy_instance', 'job_type', 'status', 'items_processed',
        'items_total', 'items_failed', 'started_at', 'completed_at'
    ]
    list_filter = [
        'job_type', 'status', 'galaxy_instance', 'started_at', 'completed_at'
    ]
    search_fields = ['error_message', 'galaxy_instance__name']
    readonly_fields = ['created_at']


@admin.register(GalaxyAPIKey)
class GalaxyAPIKeyAdmin(admin.ModelAdmin):
    list_display = [
        'key_name', 'galaxy_instance', 'is_active', 'created_at',
        'expires_at', 'last_used', 'usage_count'
    ]
    list_filter = [
        'is_active', 'galaxy_instance', 'created_at', 'expires_at'
    ]
    search_fields = [
        'key_name', 'galaxy_instance__name'
    ]
    readonly_fields = ['created_at', 'last_used', 'usage_count']