from django.contrib import admin
from .models import (
    AnnotationSource, AnnotationJob, VariantAnnotation, ClinVarAnnotation,
    COSMICAnnotation, CIViCAnnotation, AnnotationCache
)


@admin.register(AnnotationSource)
class AnnotationSourceAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'version', 'is_active', 'last_updated', 'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AnnotationJob)
class AnnotationJobAdmin(admin.ModelAdmin):
    list_display = [
        'job_id', 'source', 'status', 'variant_count', 'processed_count',
        'failed_count', 'started_at', 'completed_at'
    ]
    list_filter = [
        'status', 'source', 'started_at', 'completed_at'
    ]
    search_fields = ['job_id', 'error_message']
    readonly_fields = ['created_at', 'job_id']


@admin.register(VariantAnnotation)
class VariantAnnotationAdmin(admin.ModelAdmin):
    list_display = [
        'variant', 'source', 'is_successful', 'confidence_score', 'created_at'
    ]
    list_filter = [
        'source', 'is_successful', 'created_at'
    ]
    search_fields = [
        'variant__variant_id', 'variant__gene_symbol', 'error_message'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ClinVarAnnotation)
class ClinVarAnnotationAdmin(admin.ModelAdmin):
    list_display = [
        'clinvar_id', 'variant_annotation', 'clinical_significance',
        'review_status', 'review_date', 'created_at'
    ]
    list_filter = [
        'clinical_significance', 'review_status', 'review_date', 'created_at'
    ]
    search_fields = [
        'clinvar_id', 'variant_annotation__variant__variant_id',
        'phenotype', 'submitter'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(COSMICAnnotation)
class COSMICAnnotationAdmin(admin.ModelAdmin):
    list_display = [
        'cosmic_id', 'variant_annotation', 'primary_site', 'primary_histology',
        'mutation_frequency', 'mutation_count', 'created_at'
    ]
    list_filter = [
        'primary_site', 'primary_histology', 'tumour_origin', 'created_at'
    ]
    search_fields = [
        'cosmic_id', 'variant_annotation__variant__variant_id',
        'primary_site', 'primary_histology', 'sample_name'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CIViCAnnotation)
class CIViCAnnotationAdmin(admin.ModelAdmin):
    list_display = [
        'civic_id', 'variant_annotation', 'drug_name', 'response_type',
        'evidence_level', 'evidence_direction', 'cancer_type', 'created_at'
    ]
    list_filter = [
        'response_type', 'evidence_level', 'evidence_direction',
        'cancer_type', 'created_at'
    ]
    search_fields = [
        'civic_id', 'variant_annotation__variant__variant_id',
        'drug_name', 'cancer_type', 'evidence_description'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AnnotationCache)
class AnnotationCacheAdmin(admin.ModelAdmin):
    list_display = [
        'cache_key', 'variant', 'hit_count', 'created_at', 'expires_at'
    ]
    list_filter = ['created_at', 'expires_at']
    search_fields = ['cache_key', 'variant__variant_id']
    readonly_fields = ['created_at', 'hit_count']