import django_filters
from django.db.models import Q
from .models import Variant, ClinicalSignificance


class VariantFilter(django_filters.FilterSet):
    """Filter for Variant model"""
    
    # Basic variant filters
    chromosome = django_filters.CharFilter(field_name='chromosome', lookup_expr='iexact')
    gene_symbol = django_filters.CharFilter(field_name='gene_symbol', lookup_expr='icontains')
    variant_id = django_filters.CharFilter(field_name='variant_id', lookup_expr='icontains')
    
    # Position range filters
    position_min = django_filters.NumberFilter(field_name='position', lookup_expr='gte')
    position_max = django_filters.NumberFilter(field_name='position', lookup_expr='lte')
    
    # Quality filters
    quality_min = django_filters.NumberFilter(field_name='quality_score', lookup_expr='gte')
    quality_max = django_filters.NumberFilter(field_name='quality_score', lookup_expr='lte')
    
    # Impact and consequence filters
    impact = django_filters.ChoiceFilter(
        choices=[('HIGH', 'HIGH'), ('MODERATE', 'MODERATE'), ('LOW', 'LOW'), ('MODIFIER', 'MODIFIER')]
    )
    consequence = django_filters.CharFilter(field_name='consequence', lookup_expr='icontains')
    
    # Population frequency filters
    gnomad_af_min = django_filters.NumberFilter(field_name='gnomad_af', lookup_expr='gte')
    gnomad_af_max = django_filters.NumberFilter(field_name='gnomad_af', lookup_expr='lte')
    
    # Clinical significance filters
    has_clinical_significance = django_filters.BooleanFilter(
        method='filter_has_clinical_significance'
    )
    clinical_significance = django_filters.CharFilter(
        method='filter_clinical_significance'
    )
    
    # Drug response filters
    has_drug_response = django_filters.BooleanFilter(
        method='filter_has_drug_response'
    )
    drug_name = django_filters.CharFilter(
        method='filter_drug_name'
    )
    
    # COSMIC filters
    has_cosmic_data = django_filters.BooleanFilter(
        method='filter_has_cosmic_data'
    )
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = Variant
        fields = [
            'chromosome', 'gene_symbol', 'variant_id', 'position_min', 'position_max',
            'quality_min', 'quality_max', 'impact', 'consequence', 'gnomad_af_min',
            'gnomad_af_max', 'has_clinical_significance', 'clinical_significance',
            'has_drug_response', 'drug_name', 'has_cosmic_data', 'created_after',
            'created_before'
        ]
    
    def filter_has_clinical_significance(self, queryset, name, value):
        """Filter variants that have clinical significance data"""
        if value:
            return queryset.filter(clinical_significance__isnull=False).distinct()
        else:
            return queryset.filter(clinical_significance__isnull=True)
    
    def filter_clinical_significance(self, queryset, name, value):
        """Filter variants by clinical significance"""
        return queryset.filter(clinical_significance__significance__icontains=value).distinct()
    
    def filter_has_drug_response(self, queryset, name, value):
        """Filter variants that have drug response data"""
        if value:
            return queryset.filter(drug_responses__isnull=False).distinct()
        else:
            return queryset.filter(drug_responses__isnull=True)
    
    def filter_drug_name(self, queryset, name, value):
        """Filter variants by drug name"""
        return queryset.filter(drug_responses__drug_name__icontains=value).distinct()
    
    def filter_has_cosmic_data(self, queryset, name, value):
        """Filter variants that have COSMIC data"""
        if value:
            return queryset.filter(cosmic_data__isnull=False).distinct()
        else:
            return queryset.filter(cosmic_data__isnull=True)


class ClinicalSignificanceFilter(django_filters.FilterSet):
    """Filter for ClinicalSignificance model"""
    
    significance = django_filters.ChoiceFilter(
        choices=ClinicalSignificance.SIGNIFICANCE_CHOICES
    )
    review_status = django_filters.CharFilter(field_name='review_status', lookup_expr='icontains')
    clinvar_id = django_filters.CharFilter(field_name='clinvar_id', lookup_expr='icontains')
    phenotype = django_filters.CharFilter(field_name='phenotype', lookup_expr='icontains')
    evidence_level = django_filters.CharFilter(field_name='evidence_level', lookup_expr='icontains')
    
    # Variant filters
    variant_id = django_filters.CharFilter(field_name='variant__variant_id', lookup_expr='icontains')
    gene_symbol = django_filters.CharFilter(field_name='variant__gene_symbol', lookup_expr='icontains')
    chromosome = django_filters.CharFilter(field_name='variant__chromosome', lookup_expr='iexact')
    
    # Date filters
    review_date_after = django_filters.DateFilter(field_name='review_date', lookup_expr='gte')
    review_date_before = django_filters.DateFilter(field_name='review_date', lookup_expr='lte')
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    class Meta:
        model = ClinicalSignificance
        fields = [
            'significance', 'review_status', 'clinvar_id', 'phenotype',
            'evidence_level', 'variant_id', 'gene_symbol', 'chromosome',
            'review_date_after', 'review_date_before', 'created_after', 'created_before'
        ]


class VariantSearchFilter(django_filters.FilterSet):
    """Advanced search filter for variants"""
    
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Variant
        fields = ['search']
    
    def filter_search(self, queryset, name, value):
        """Multi-field search across variant data"""
        if not value:
            return queryset
        
        return queryset.filter(
            Q(variant_id__icontains=value) |
            Q(gene_symbol__icontains=value) |
            Q(hgvs_c__icontains=value) |
            Q(hgvs_p__icontains=value) |
            Q(consequence__icontains=value) |
            Q(clinical_significance__phenotype__icontains=value) |
            Q(drug_responses__drug_name__icontains=value)
        ).distinct()
