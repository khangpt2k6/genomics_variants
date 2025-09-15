import django_filters
from django.db.models import Q
from .models import AnnotationJob, VariantAnnotation


class AnnotationJobFilter(django_filters.FilterSet):
    """Filter for AnnotationJob model"""
    
    # Basic filters
    status = django_filters.ChoiceFilter(
        choices=AnnotationJob.STATUS_CHOICES
    )
    source_name = django_filters.CharFilter(field_name='source__name', lookup_expr='icontains')
    
    # Count filters
    variant_count_min = django_filters.NumberFilter(field_name='variant_count', lookup_expr='gte')
    variant_count_max = django_filters.NumberFilter(field_name='variant_count', lookup_expr='lte')
    processed_count_min = django_filters.NumberFilter(field_name='processed_count', lookup_expr='gte')
    processed_count_max = django_filters.NumberFilter(field_name='processed_count', lookup_expr='lte')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    started_after = django_filters.DateTimeFilter(field_name='started_at', lookup_expr='gte')
    started_before = django_filters.DateTimeFilter(field_name='started_at', lookup_expr='lte')
    completed_after = django_filters.DateTimeFilter(field_name='completed_at', lookup_expr='gte')
    completed_before = django_filters.DateTimeFilter(field_name='completed_at', lookup_expr='lte')
    
    # Error filters
    has_error = django_filters.BooleanFilter(
        method='filter_has_error'
    )
    error_message = django_filters.CharFilter(
        field_name='error_message', lookup_expr='icontains'
    )
    
    # Retry filters
    retry_count_min = django_filters.NumberFilter(field_name='retry_count', lookup_expr='gte')
    retry_count_max = django_filters.NumberFilter(field_name='retry_count', lookup_expr='lte')
    
    class Meta:
        model = AnnotationJob
        fields = [
            'status', 'source_name', 'variant_count_min', 'variant_count_max',
            'processed_count_min', 'processed_count_max', 'created_after',
            'created_before', 'started_after', 'started_before', 'completed_after',
            'completed_before', 'has_error', 'error_message', 'retry_count_min',
            'retry_count_max'
        ]
    
    def filter_has_error(self, queryset, name, value):
        """Filter jobs that have errors"""
        if value:
            return queryset.exclude(error_message='')
        else:
            return queryset.filter(error_message='')


class VariantAnnotationFilter(django_filters.FilterSet):
    """Filter for VariantAnnotation model"""
    
    # Basic filters
    is_successful = django_filters.BooleanFilter()
    source_name = django_filters.CharFilter(field_name='source__name', lookup_expr='icontains')
    job_id = django_filters.CharFilter(field_name='job__job_id', lookup_expr='icontains')
    
    # Variant filters
    variant_id = django_filters.CharFilter(field_name='variant__variant_id', lookup_expr='icontains')
    gene_symbol = django_filters.CharFilter(field_name='variant__gene_symbol', lookup_expr='icontains')
    chromosome = django_filters.CharFilter(field_name='variant__chromosome', lookup_expr='iexact')
    
    # Confidence score filters
    confidence_score_min = django_filters.NumberFilter(field_name='confidence_score', lookup_expr='gte')
    confidence_score_max = django_filters.NumberFilter(field_name='confidence_score', lookup_expr='lte')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    
    # Error filters
    has_error = django_filters.BooleanFilter(
        method='filter_has_error'
    )
    error_message = django_filters.CharFilter(
        field_name='error_message', lookup_expr='icontains'
    )
    
    class Meta:
        model = VariantAnnotation
        fields = [
            'is_successful', 'source_name', 'job_id', 'variant_id', 'gene_symbol',
            'chromosome', 'confidence_score_min', 'confidence_score_max',
            'created_after', 'created_before', 'updated_after', 'updated_before',
            'has_error', 'error_message'
        ]
    
    def filter_has_error(self, queryset, name, value):
        """Filter annotations that have errors"""
        if value:
            return queryset.exclude(error_message='')
        else:
            return queryset.filter(error_message='')


class ClinVarAnnotationFilter(django_filters.FilterSet):
    """Filter for ClinVarAnnotation model"""
    
    # Basic filters
    clinical_significance = django_filters.CharFilter(field_name='clinical_significance', lookup_expr='icontains')
    review_status = django_filters.CharFilter(field_name='review_status', lookup_expr='icontains')
    clinvar_id = django_filters.CharFilter(field_name='clinvar_id', lookup_expr='icontains')
    phenotype = django_filters.CharFilter(field_name='phenotype', lookup_expr='icontains')
    evidence_level = django_filters.CharFilter(field_name='evidence_level', lookup_expr='icontains')
    
    # Variant filters
    variant_id = django_filters.CharFilter(field_name='variant_annotation__variant__variant_id', lookup_expr='icontains')
    gene_symbol = django_filters.CharFilter(field_name='variant_annotation__variant__gene_symbol', lookup_expr='icontains')
    chromosome = django_filters.CharFilter(field_name='variant_annotation__variant__chromosome', lookup_expr='iexact')
    
    # Date filters
    review_date_after = django_filters.DateFilter(field_name='review_date', lookup_expr='gte')
    review_date_before = django_filters.DateFilter(field_name='review_date', lookup_expr='lte')
    submission_date_after = django_filters.DateFilter(field_name='submission_date', lookup_expr='gte')
    submission_date_before = django_filters.DateFilter(field_name='submission_date', lookup_expr='lte')
    
    class Meta:
        model = 'annotations.ClinVarAnnotation'
        fields = [
            'clinical_significance', 'review_status', 'clinvar_id', 'phenotype',
            'evidence_level', 'variant_id', 'gene_symbol', 'chromosome',
            'review_date_after', 'review_date_before', 'submission_date_after',
            'submission_date_before'
        ]


class COSMICAnnotationFilter(django_filters.FilterSet):
    """Filter for COSMICAnnotation model"""
    
    # Basic filters
    cosmic_id = django_filters.CharFilter(field_name='cosmic_id', lookup_expr='icontains')
    primary_site = django_filters.CharFilter(field_name='primary_site', lookup_expr='icontains')
    primary_histology = django_filters.CharFilter(field_name='primary_histology', lookup_expr='icontains')
    site_subtype = django_filters.CharFilter(field_name='site_subtype', lookup_expr='icontains')
    histology_subtype = django_filters.CharFilter(field_name='histology_subtype', lookup_expr='icontains')
    
    # Variant filters
    variant_id = django_filters.CharFilter(field_name='variant_annotation__variant__variant_id', lookup_expr='icontains')
    gene_symbol = django_filters.CharFilter(field_name='variant_annotation__variant__gene_symbol', lookup_expr='icontains')
    chromosome = django_filters.CharFilter(field_name='variant_annotation__variant__chromosome', lookup_expr='iexact')
    
    # Frequency filters
    mutation_frequency_min = django_filters.NumberFilter(field_name='mutation_frequency', lookup_expr='gte')
    mutation_frequency_max = django_filters.NumberFilter(field_name='mutation_frequency', lookup_expr='lte')
    mutation_count_min = django_filters.NumberFilter(field_name='mutation_count', lookup_expr='gte')
    mutation_count_max = django_filters.NumberFilter(field_name='mutation_count', lookup_expr='lte')
    
    class Meta:
        model = 'annotations.COSMICAnnotation'
        fields = [
            'cosmic_id', 'primary_site', 'primary_histology', 'site_subtype',
            'histology_subtype', 'variant_id', 'gene_symbol', 'chromosome',
            'mutation_frequency_min', 'mutation_frequency_max', 'mutation_count_min',
            'mutation_count_max'
        ]


class CIViCAnnotationFilter(django_filters.FilterSet):
    """Filter for CIViCAnnotation model"""
    
    # Basic filters
    civic_id = django_filters.CharFilter(field_name='civic_id', lookup_expr='icontains')
    drug_name = django_filters.CharFilter(field_name='drug_name', lookup_expr='icontains')
    response_type = django_filters.CharFilter(field_name='response_type', lookup_expr='icontains')
    evidence_level = django_filters.CharFilter(field_name='evidence_level', lookup_expr='icontains')
    evidence_direction = django_filters.CharFilter(field_name='evidence_direction', lookup_expr='icontains')
    cancer_type = django_filters.CharFilter(field_name='cancer_type', lookup_expr='icontains')
    tissue_type = django_filters.CharFilter(field_name='tissue_type', lookup_expr='icontains')
    
    # Variant filters
    variant_id = django_filters.CharFilter(field_name='variant_annotation__variant__variant_id', lookup_expr='icontains')
    gene_symbol = django_filters.CharFilter(field_name='variant_annotation__variant__gene_symbol', lookup_expr='icontains')
    chromosome = django_filters.CharFilter(field_name='variant_annotation__variant__chromosome', lookup_expr='iexact')
    
    class Meta:
        model = 'annotations.CIViCAnnotation'
        fields = [
            'civic_id', 'drug_name', 'response_type', 'evidence_level',
            'evidence_direction', 'cancer_type', 'tissue_type', 'variant_id',
            'gene_symbol', 'chromosome'
        ]


class AnnotationCacheFilter(django_filters.FilterSet):
    """Filter for AnnotationCache model"""
    
    # Basic filters
    cache_key = django_filters.CharFilter(field_name='cache_key', lookup_expr='icontains')
    variant_id = django_filters.CharFilter(field_name='variant__variant_id', lookup_expr='icontains')
    gene_symbol = django_filters.CharFilter(field_name='variant__gene_symbol', lookup_expr='icontains')
    
    # Hit count filters
    hit_count_min = django_filters.NumberFilter(field_name='hit_count', lookup_expr='gte')
    hit_count_max = django_filters.NumberFilter(field_name='hit_count', lookup_expr='lte')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    expires_after = django_filters.DateTimeFilter(field_name='expires_at', lookup_expr='gte')
    expires_before = django_filters.DateTimeFilter(field_name='expires_at', lookup_expr='lte')
    
    # Expiry filters
    is_expired = django_filters.BooleanFilter(
        method='filter_is_expired'
    )
    
    class Meta:
        model = 'annotations.AnnotationCache'
        fields = [
            'cache_key', 'variant_id', 'gene_symbol', 'hit_count_min',
            'hit_count_max', 'created_after', 'created_before', 'expires_after',
            'expires_before', 'is_expired'
        ]
    
    def filter_is_expired(self, queryset, name, value):
        """Filter expired cache entries"""
        from django.utils import timezone
        
        if value:
            return queryset.filter(expires_at__lt=timezone.now())
        else:
            return queryset.filter(expires_at__gte=timezone.now())
