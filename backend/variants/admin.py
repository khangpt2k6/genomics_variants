from django.contrib import admin
from .models import (
    Variant, ClinicalSignificance, DrugResponse, COSMICData, VariantAnnotation
)


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = [
        'variant_id', 'chromosome', 'position', 'reference_allele', 
        'alternate_allele', 'gene_symbol', 'consequence', 'impact', 'created_at'
    ]
    list_filter = [
        'chromosome', 'consequence', 'impact', 'created_at'
    ]
    search_fields = [
        'variant_id', 'gene_symbol', 'hgvs_c', 'hgvs_p'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['chromosome', 'position']


@admin.register(ClinicalSignificance)
class ClinicalSignificanceAdmin(admin.ModelAdmin):
    list_display = [
        'variant', 'significance', 'review_status', 'review_date', 
        'clinvar_id', 'created_at'
    ]
    list_filter = [
        'significance', 'review_status', 'review_date', 'created_at'
    ]
    search_fields = [
        'variant__variant_id', 'clinvar_id', 'phenotype'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DrugResponse)
class DrugResponseAdmin(admin.ModelAdmin):
    list_display = [
        'variant', 'drug_name', 'response_type', 'evidence_level', 
        'evidence_direction', 'cancer_type', 'created_at'
    ]
    list_filter = [
        'response_type', 'evidence_level', 'evidence_direction', 
        'cancer_type', 'created_at'
    ]
    search_fields = [
        'variant__variant_id', 'drug_name', 'cancer_type', 'civic_id'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(COSMICData)
class COSMICDataAdmin(admin.ModelAdmin):
    list_display = [
        'cosmic_id', 'variant', 'primary_site', 'primary_histology', 
        'mutation_frequency', 'mutation_count', 'created_at'
    ]
    list_filter = [
        'primary_site', 'primary_histology', 'tumour_origin', 'created_at'
    ]
    search_fields = [
        'cosmic_id', 'variant__variant_id', 'primary_site', 
        'primary_histology', 'sample_name'
    ]
    readonly_fields = ['created_at', 'updated_at']


@admin.register(VariantAnnotation)
class VariantAnnotationAdmin(admin.ModelAdmin):
    list_display = [
        'variant', 'is_pathogenic', 'is_drug_target', 'has_cosmic_data',
        'pathogenicity_score', 'drug_response_score', 'annotation_date'
    ]
    list_filter = [
        'is_pathogenic', 'is_drug_target', 'has_cosmic_data', 
        'annotation_date'
    ]
    search_fields = [
        'variant__variant_id', 'variant__gene_symbol'
    ]
    readonly_fields = ['annotation_date']