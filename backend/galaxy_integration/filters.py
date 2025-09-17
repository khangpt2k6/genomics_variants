import django_filters
from django.db.models import Q
from .models import GalaxyHistory, GalaxyDataset, GalaxyWorkflow, GalaxySyncJob


class GalaxyHistoryFilter(django_filters.FilterSet):
    """Filter for GalaxyHistory model"""
    
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=GalaxyHistory.STATUS_CHOICES)
    galaxy_instance = django_filters.NumberFilter(field_name='galaxy_instance__id')
    galaxy_instance_name = django_filters.CharFilter(field_name='galaxy_instance__name', lookup_expr='icontains')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    galaxy_created_after = django_filters.DateTimeFilter(field_name='galaxy_created_at', lookup_expr='gte')
    galaxy_created_before = django_filters.DateTimeFilter(field_name='galaxy_created_at', lookup_expr='lte')
    
    class Meta:
        model = GalaxyHistory
        fields = [
            'name', 'status', 'galaxy_instance', 'galaxy_instance_name',
            'created_after', 'created_before', 'galaxy_created_after', 'galaxy_created_before'
        ]


class GalaxyDatasetFilter(django_filters.FilterSet):
    """Filter for GalaxyDataset model"""
    
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    file_type = django_filters.CharFilter(field_name='file_type', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=GalaxyDataset.STATUS_CHOICES)
    galaxy_instance = django_filters.NumberFilter(field_name='galaxy_instance__id')
    galaxy_instance_name = django_filters.CharFilter(field_name='galaxy_instance__name', lookup_expr='icontains')
    galaxy_history = django_filters.NumberFilter(field_name='galaxy_history__id')
    galaxy_history_name = django_filters.CharFilter(field_name='galaxy_history__name', lookup_expr='icontains')
    
    # VCF specific filters
    is_vcf = django_filters.BooleanFilter(field_name='is_vcf')
    is_processed = django_filters.BooleanFilter(field_name='is_processed')
    
    # File size filters
    file_size_min = django_filters.NumberFilter(field_name='file_size', lookup_expr='gte')
    file_size_max = django_filters.NumberFilter(field_name='file_size', lookup_expr='lte')
    
    # VCF count filters
    vcf_sample_count_min = django_filters.NumberFilter(field_name='vcf_sample_count', lookup_expr='gte')
    vcf_sample_count_max = django_filters.NumberFilter(field_name='vcf_sample_count', lookup_expr='lte')
    vcf_variant_count_min = django_filters.NumberFilter(field_name='vcf_variant_count', lookup_expr='gte')
    vcf_variant_count_max = django_filters.NumberFilter(field_name='vcf_variant_count', lookup_expr='lte')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    processing_started_after = django_filters.DateTimeFilter(field_name='processing_started_at', lookup_expr='gte')
    processing_started_before = django_filters.DateTimeFilter(field_name='processing_started_at', lookup_expr='lte')
    
    class Meta:
        model = GalaxyDataset
        fields = [
            'name', 'file_type', 'status', 'galaxy_instance', 'galaxy_instance_name',
            'galaxy_history', 'galaxy_history_name', 'is_vcf', 'is_processed',
            'file_size_min', 'file_size_max', 'vcf_sample_count_min', 'vcf_sample_count_max',
            'vcf_variant_count_min', 'vcf_variant_count_max', 'created_after',
            'created_before', 'processing_started_after', 'processing_started_before'
        ]


class GalaxyWorkflowFilter(django_filters.FilterSet):
    """Filter for GalaxyWorkflow model"""
    
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    status = django_filters.ChoiceFilter(choices=GalaxyWorkflow.STATUS_CHOICES)
    galaxy_instance = django_filters.NumberFilter(field_name='galaxy_instance__id')
    galaxy_instance_name = django_filters.CharFilter(field_name='galaxy_instance__name', lookup_expr='icontains')
    version = django_filters.CharFilter(field_name='version', lookup_expr='icontains')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    started_after = django_filters.DateTimeFilter(field_name='started_at', lookup_expr='gte')
    started_before = django_filters.DateTimeFilter(field_name='started_at', lookup_expr='lte')
    completed_after = django_filters.DateTimeFilter(field_name='completed_at', lookup_expr='gte')
    completed_before = django_filters.DateTimeFilter(field_name='completed_at', lookup_expr='lte')
    
    class Meta:
        model = GalaxyWorkflow
        fields = [
            'name', 'status', 'galaxy_instance', 'galaxy_instance_name', 'version',
            'created_after', 'created_before', 'started_after', 'started_before',
            'completed_after', 'completed_before'
        ]


class GalaxySyncJobFilter(django_filters.FilterSet):
    """Filter for GalaxySyncJob model"""
    
    job_type = django_filters.ChoiceFilter(choices=[
        ('history', 'History'),
        ('dataset', 'Dataset'),
        ('workflow', 'Workflow')
    ])
    status = django_filters.ChoiceFilter(choices=GalaxySyncJob.STATUS_CHOICES)
    galaxy_instance = django_filters.NumberFilter(field_name='galaxy_instance__id')
    galaxy_instance_name = django_filters.CharFilter(field_name='galaxy_instance__name', lookup_expr='icontains')
    
    # Progress filters
    items_processed_min = django_filters.NumberFilter(field_name='items_processed', lookup_expr='gte')
    items_processed_max = django_filters.NumberFilter(field_name='items_processed', lookup_expr='lte')
    items_total_min = django_filters.NumberFilter(field_name='items_total', lookup_expr='gte')
    items_total_max = django_filters.NumberFilter(field_name='items_total', lookup_expr='lte')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    started_after = django_filters.DateTimeFilter(field_name='started_at', lookup_expr='gte')
    started_before = django_filters.DateTimeFilter(field_name='started_at', lookup_expr='lte')
    
    class Meta:
        model = GalaxySyncJob
        fields = [
            'job_type', 'status', 'galaxy_instance', 'galaxy_instance_name',
            'items_processed_min', 'items_processed_max', 'items_total_min', 'items_total_max',
            'created_after', 'created_before', 'started_after', 'started_before'
        ]


class GalaxyDatasetSearchFilter(django_filters.FilterSet):
    """Advanced search filter for Galaxy datasets"""
    
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = GalaxyDataset
        fields = ['search']
    
    def filter_search(self, queryset, name, value):
        """Multi-field search across dataset data"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(name__icontains=value) |
            Q(file_type__icontains=value) |
            Q(galaxy_history__name__icontains=value) |
            Q(galaxy_instance__name__icontains=value) |
            Q(error_message__icontains=value)
        ).distinct()
