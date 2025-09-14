from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator, MaxValueValidator


class Variant(models.Model):
    """Represents a genetic variant from VCF data"""
    
    # Basic variant information
    chromosome = models.CharField(max_length=10)
    position = models.PositiveIntegerField()
    reference_allele = models.CharField(max_length=100)
    alternate_allele = models.CharField(max_length=100)
    variant_id = models.CharField(max_length=100, unique=True, db_index=True)
    
    # VCF quality metrics
    quality_score = models.FloatField(null=True, blank=True)
    filter_status = models.CharField(max_length=50, null=True, blank=True)
    
    # Genomic context
    gene_symbol = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    transcript_id = models.CharField(max_length=100, null=True, blank=True)
    hgvs_c = models.CharField(max_length=200, null=True, blank=True)  # cDNA notation
    hgvs_p = models.CharField(max_length=200, null=True, blank=True)  # protein notation
    
    # Functional impact
    consequence = models.CharField(max_length=100, null=True, blank=True)
    impact = models.CharField(max_length=20, null=True, blank=True)  # HIGH, MODERATE, LOW, MODIFIER
    
    # Population frequencies
    gnomad_af = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    gnomad_af_afr = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    gnomad_af_amr = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    gnomad_af_eas = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    gnomad_af_nfe = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    gnomad_af_sas = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional VCF data as JSON
    vcf_data = JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['chromosome', 'position']
        indexes = [
            models.Index(fields=['chromosome', 'position']),
            models.Index(fields=['gene_symbol']),
            models.Index(fields=['variant_id']),
        ]
    
    def __str__(self):
        return f"{self.chromosome}:{self.position} {self.reference_allele}>{self.alternate_allele}"


class ClinicalSignificance(models.Model):
    """Clinical significance data from ClinVar"""
    
    SIGNIFICANCE_CHOICES = [
        ('pathogenic', 'Pathogenic'),
        ('likely_pathogenic', 'Likely Pathogenic'),
        ('uncertain_significance', 'Uncertain Significance'),
        ('likely_benign', 'Likely Benign'),
        ('benign', 'Benign'),
        ('conflicting', 'Conflicting Interpretations'),
    ]
    
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='clinical_significance')
    significance = models.CharField(max_length=30, choices=SIGNIFICANCE_CHOICES)
    review_status = models.CharField(max_length=50, null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)
    clinvar_id = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    
    # Evidence details
    evidence_level = models.CharField(max_length=50, null=True, blank=True)
    phenotype = models.TextField(null=True, blank=True)
    inheritance_pattern = models.CharField(max_length=50, null=True, blank=True)
    
    # Additional ClinVar data
    clinvar_data = JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-review_date', 'significance']
        unique_together = ['variant', 'clinvar_id']
    
    def __str__(self):
        return f"{self.variant} - {self.significance}"


class DrugResponse(models.Model):
    """Drug response information from CIViC"""
    
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='drug_responses')
    drug_name = models.CharField(max_length=200)
    response_type = models.CharField(max_length=50)  # sensitivity, resistance, etc.
    evidence_level = models.CharField(max_length=20)  # A, B, C, D
    evidence_direction = models.CharField(max_length=20)  # supports, does not support
    
    # CIViC specific fields
    civic_id = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    evidence_id = models.CharField(max_length=50, null=True, blank=True)
    
    # Clinical context
    cancer_type = models.CharField(max_length=200, null=True, blank=True)
    tissue_type = models.CharField(max_length=100, null=True, blank=True)
    
    # Additional CIViC data
    civic_data = JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['drug_name', 'evidence_level']
        unique_together = ['variant', 'civic_id']
    
    def __str__(self):
        return f"{self.variant} - {self.drug_name} ({self.response_type})"


class COSMICData(models.Model):
    """COSMIC database information"""
    
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='cosmic_data')
    cosmic_id = models.CharField(max_length=50, unique=True, db_index=True)
    
    # COSMIC specific fields
    mutation_description = models.TextField(null=True, blank=True)
    mutation_cds = models.CharField(max_length=200, null=True, blank=True)
    mutation_aa = models.CharField(max_length=200, null=True, blank=True)
    
    # Cancer information
    primary_site = models.CharField(max_length=100, null=True, blank=True)
    site_subtype = models.CharField(max_length=100, null=True, blank=True)
    primary_histology = models.CharField(max_length=100, null=True, blank=True)
    histology_subtype = models.CharField(max_length=100, null=True, blank=True)
    
    # Sample information
    sample_name = models.CharField(max_length=100, null=True, blank=True)
    sample_source = models.CharField(max_length=100, null=True, blank=True)
    tumour_origin = models.CharField(max_length=50, null=True, blank=True)
    
    # Frequency data
    mutation_frequency = models.FloatField(null=True, blank=True)
    mutation_count = models.PositiveIntegerField(null=True, blank=True)
    
    # Additional COSMIC data
    cosmic_data = JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['cosmic_id']
    
    def __str__(self):
        return f"{self.cosmic_id} - {self.primary_site}"


class VariantAnnotation(models.Model):
    """Combined annotation data for a variant"""
    
    variant = models.OneToOneField(Variant, on_delete=models.CASCADE, related_name='annotation')
    
    # Summary fields
    is_pathogenic = models.BooleanField(default=False)
    is_drug_target = models.BooleanField(default=False)
    has_cosmic_data = models.BooleanField(default=False)
    
    # Risk scores
    pathogenicity_score = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    drug_response_score = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Annotation metadata
    annotation_date = models.DateTimeField(auto_now=True)
    annotation_version = models.CharField(max_length=20, default='1.0')
    
    # Combined annotation data
    annotation_data = JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-annotation_date']
    
    def __str__(self):
        return f"Annotation for {self.variant}"