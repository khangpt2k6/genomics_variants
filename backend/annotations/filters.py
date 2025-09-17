import django_filters
from django.db.models import Q
from .models import AnnotationJob, VariantAnnotation


class AnnotationJobFilter(django_filters.FilterSet):
    """Filter for AnnotationJob model"""
    
    status = django_filters.ChoiceFilter(choices=AnnotationJob.STATUS_CHOICES)
    source = django_filters.NumberFilter(field_name='source__id')
    source_name = django_filters.CharFilter(field_name='source__name', lookup_expr='icontains')
    
    # Progress filters
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
    
    class Meta:
        model = AnnotationJob
        fields = [
            'status', 'source', 'source_name', 'variant_count_min', 'variant_count_max',
            'processed_count_min', 'processed_count_max', 'created_after', 'created_before',
            'started_after', 'started_before', 'completed_after', 'completed_before'
        ]


class VariantAnnotationFilter(django_filters.FilterSet):
    """Filter for VariantAnnotation model"""
    
    variant_id = django_filters.NumberFilter(field_name='variant__id')
    variant_display = django_filters.CharFilter(field_name='variant__variant_id', lookup_expr='icontains')
    source = django_filters.NumberFilter(field_name='source__id')
    source_name = django_filters.CharFilter(field_name='source__name', lookup_expr='icontains')
    job = django_filters.NumberFilter(field_name='job__id')
    is_successful = django_filters.BooleanFilter(field_name='is_successful')
    
    # Confidence score filters
    confidence_score_min = django_filters.NumberFilter(field_name='confidence_score', lookup_expr='gte')
    confidence_score_max = django_filters.NumberFilter(field_name='confidence_score', lookup_expr='lte')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = VariantAnnotation
        fields = [
            'variant_id', 'variant_display', 'source', 'source_name', 'job',
            'is_successful', 'confidence_score_min', 'confidence_score_max',
            'created_after', 'created_before'
        ]


class AnnotationSearchFilter(django_filters.FilterSet):
    """Advanced search filter for annotations"""
    
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = VariantAnnotation
        fields = ['search']
    
    def filter_search(self, queryset, name, value):
        """Multi-field search across annotation data"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(variant__variant_id__icontains=value) |
            Q(variant__gene_symbol__icontains=value) |
            Q(source__name__icontains=value) |
            Q(error_message__icontains=value)
        ).distinct()