"""
Django models for the Variants application.

This module contains all the database models for storing genetic variant data,
clinical significance information, drug responses, and annotations.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class Variant(models.Model):
    """
    Represents a genetic variant from VCF data.
    
    This model stores the core variant information including genomic coordinates,
    alleles, quality metrics, and population frequencies from gnomAD.
    """
    
    # =============================================================================
    # CHOICES
    # =============================================================================
    
    IMPACT_CHOICES = [
        ('HIGH', 'High'),
        ('MODERATE', 'Moderate'),
        ('LOW', 'Low'),
        ('MODIFIER', 'Modifier'),
    ]
    
    # =============================================================================
    # BASIC VARIANT INFORMATION
    # =============================================================================
    
    chromosome = models.CharField(
        max_length=10,
        help_text="Chromosome identifier (e.g., '1', 'X', 'MT')"
    )
    position = models.PositiveIntegerField(
        help_text="Genomic position (1-based)"
    )
    reference_allele = models.CharField(
        max_length=100,
        help_text="Reference allele sequence"
    )
    alternate_allele = models.CharField(
        max_length=100,
        help_text="Alternate allele sequence"
    )
    variant_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique variant identifier"
    )
    
    # =============================================================================
    # VCF QUALITY METRICS
    # =============================================================================
    
    quality_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="VCF quality score (QUAL field)"
    )
    filter_status = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="VCF filter status (FILTER field)"
    )
    
    # =============================================================================
    # GENOMIC CONTEXT
    # =============================================================================
    
    gene_symbol = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        help_text="Gene symbol (e.g., 'BRCA1')"
    )
    transcript_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Transcript identifier"
    )
    hgvs_c = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="HGVS cDNA notation"
    )
    hgvs_p = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="HGVS protein notation"
    )
    
    # =============================================================================
    # FUNCTIONAL IMPACT
    # =============================================================================
    
    consequence = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Variant consequence (e.g., 'missense_variant')"
    )
    impact = models.CharField(
        max_length=20,
        choices=IMPACT_CHOICES,
        null=True,
        blank=True,
        help_text="Predicted functional impact"
    )
    
    # =============================================================================
    # POPULATION FREQUENCIES
    # =============================================================================
    
    gnomad_af = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="gnomAD allele frequency (global)"
    )
    gnomad_af_afr = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="gnomAD allele frequency (African/African American)"
    )
    gnomad_af_amr = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="gnomAD allele frequency (Latino/Admixed American)"
    )
    gnomad_af_eas = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="gnomAD allele frequency (East Asian)"
    )
    gnomad_af_nfe = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="gnomAD allele frequency (Non-Finnish European)"
    )
    gnomad_af_sas = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="gnomAD allele frequency (South Asian)"
    )
    
    # =============================================================================
    # TIMESTAMPS
    # =============================================================================
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # =============================================================================
    # ADDITIONAL DATA
    # =============================================================================
    
    vcf_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional VCF data as JSON"
    )
    
    class Meta:
        ordering = ['chromosome', 'position']
        indexes = [
            models.Index(fields=['chromosome', 'position']),
            models.Index(fields=['gene_symbol']),
            models.Index(fields=['variant_id']),
            models.Index(fields=['impact']),
            models.Index(fields=['consequence']),
        ]
        verbose_name = "Genetic Variant"
        verbose_name_plural = "Genetic Variants"
    
    def __str__(self):
        return f"{self.chromosome}:{self.position} {self.reference_allele}>{self.alternate_allele}"
    
    def clean(self):
        """Validate variant data."""
        super().clean()
        
        # Validate chromosome format
        if self.chromosome and not self.chromosome.replace('chr', '').replace('X', '23').replace('Y', '24').replace('MT', '25').isdigit():
            if self.chromosome not in ['X', 'Y', 'MT', 'chrX', 'chrY', 'chrMT']:
                raise ValidationError("Invalid chromosome format")
        
        # Validate allele sequences
        if self.reference_allele and self.alternate_allele:
            if self.reference_allele == self.alternate_allele:
                raise ValidationError("Reference and alternate alleles cannot be identical")
    
    def get_gnomad_frequencies(self):
        """Return all gnomAD frequencies as a dictionary."""
        return {
            'global': self.gnomad_af,
            'afr': self.gnomad_af_afr,
            'amr': self.gnomad_af_amr,
            'eas': self.gnomad_af_eas,
            'nfe': self.gnomad_af_nfe,
            'sas': self.gnomad_af_sas,
        }
    
    def is_rare(self, threshold=0.01):
        """Check if variant is rare based on global gnomAD frequency."""
        return self.gnomad_af is not None and self.gnomad_af < threshold


class ClinicalSignificance(models.Model):
    """
    Clinical significance data from ClinVar.
    
    This model stores clinical interpretation data from the ClinVar database,
    including pathogenicity classifications and supporting evidence.
    """
    
    # =============================================================================
    # CHOICES
    # =============================================================================
    
    SIGNIFICANCE_CHOICES = [
        ('pathogenic', 'Pathogenic'),
        ('likely_pathogenic', 'Likely Pathogenic'),
        ('uncertain_significance', 'Uncertain Significance'),
        ('likely_benign', 'Likely Benign'),
        ('benign', 'Benign'),
        ('conflicting', 'Conflicting Interpretations'),
    ]
    
    REVIEW_STATUS_CHOICES = [
        ('reviewed_by_expert_panel', 'Reviewed by Expert Panel'),
        ('criteria_provided_single_submitter', 'Criteria Provided, Single Submitter'),
        ('criteria_provided_multiple_submitters', 'Criteria Provided, Multiple Submitters'),
        ('no_assertion_criteria_provided', 'No Assertion Criteria Provided'),
        ('no_assertion_provided', 'No Assertion Provided'),
    ]
    
    # =============================================================================
    # BASIC INFORMATION
    # =============================================================================
    
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name='clinical_significance',
        help_text="Associated genetic variant"
    )
    significance = models.CharField(
        max_length=30,
        choices=SIGNIFICANCE_CHOICES,
        help_text="Clinical significance classification"
    )
    review_status = models.CharField(
        max_length=50,
        choices=REVIEW_STATUS_CHOICES,
        null=True,
        blank=True,
        help_text="ClinVar review status"
    )
    review_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date of last review"
    )
    clinvar_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        help_text="ClinVar variation ID"
    )
    
    # =============================================================================
    # EVIDENCE DETAILS
    # =============================================================================
    
    evidence_level = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Evidence level (e.g., '1', '2A', '2B')"
    )
    phenotype = models.TextField(
        null=True,
        blank=True,
        help_text="Associated phenotype or condition"
    )
    inheritance_pattern = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Inheritance pattern (e.g., 'Autosomal dominant')"
    )
    
    # =============================================================================
    # ADDITIONAL DATA
    # =============================================================================
    
    clinvar_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional ClinVar data as JSON"
    )
    
    # =============================================================================
    # TIMESTAMPS
    # =============================================================================
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-review_date', 'significance']
        unique_together = ['variant', 'clinvar_id']
        verbose_name = "Clinical Significance"
        verbose_name_plural = "Clinical Significance Records"
    
    def __str__(self):
        return f"{self.variant} - {self.get_significance_display()}"
    
    def is_pathogenic(self):
        """Check if the variant is classified as pathogenic."""
        return self.significance in ['pathogenic', 'likely_pathogenic']
    
    def is_benign(self):
        """Check if the variant is classified as benign."""
        return self.significance in ['benign', 'likely_benign']
    
    def has_conflicting_interpretations(self):
        """Check if there are conflicting interpretations."""
        return self.significance == 'conflicting'


class DrugResponse(models.Model):
    """
    Drug response information from CIViC.
    
    This model stores drug response data from the CIViC database,
    including sensitivity, resistance, and supporting evidence.
    """
    
    # =============================================================================
    # CHOICES
    # =============================================================================
    
    RESPONSE_TYPE_CHOICES = [
        ('sensitivity', 'Sensitivity'),
        ('resistance', 'Resistance'),
        ('adverse_effect', 'Adverse Effect'),
        ('reduced_sensitivity', 'Reduced Sensitivity'),
        ('increased_sensitivity', 'Increased Sensitivity'),
    ]
    
    EVIDENCE_LEVEL_CHOICES = [
        ('A', 'Level A - Validated clinical utility'),
        ('B', 'Level B - Clinical evidence'),
        ('C', 'Level C - Case study'),
        ('D', 'Level D - Preclinical evidence'),
    ]
    
    EVIDENCE_DIRECTION_CHOICES = [
        ('supports', 'Supports'),
        ('does_not_support', 'Does Not Support'),
        ('inconclusive', 'Inconclusive'),
    ]
    
    # =============================================================================
    # BASIC INFORMATION
    # =============================================================================
    
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name='drug_responses',
        help_text="Associated genetic variant"
    )
    drug_name = models.CharField(
        max_length=200,
        help_text="Name of the drug"
    )
    response_type = models.CharField(
        max_length=50,
        choices=RESPONSE_TYPE_CHOICES,
        help_text="Type of drug response"
    )
    evidence_level = models.CharField(
        max_length=20,
        choices=EVIDENCE_LEVEL_CHOICES,
        help_text="Evidence level classification"
    )
    evidence_direction = models.CharField(
        max_length=20,
        choices=EVIDENCE_DIRECTION_CHOICES,
        help_text="Direction of evidence"
    )
    
    # =============================================================================
    # CIVIC SPECIFIC FIELDS
    # =============================================================================
    
    civic_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        db_index=True,
        help_text="CIViC variant ID"
    )
    evidence_id = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="CIViC evidence ID"
    )
    
    # =============================================================================
    # CLINICAL CONTEXT
    # =============================================================================
    
    cancer_type = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Type of cancer"
    )
    tissue_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Tissue type"
    )
    
    # =============================================================================
    # ADDITIONAL DATA
    # =============================================================================
    
    civic_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional CIViC data as JSON"
    )
    
    # =============================================================================
    # TIMESTAMPS
    # =============================================================================
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['drug_name', 'evidence_level']
        unique_together = ['variant', 'civic_id']
        verbose_name = "Drug Response"
        verbose_name_plural = "Drug Responses"
    
    def __str__(self):
        return f"{self.variant} - {self.drug_name} ({self.get_response_type_display()})"
    
    def is_sensitivity(self):
        """Check if the response indicates drug sensitivity."""
        return self.response_type in ['sensitivity', 'increased_sensitivity']
    
    def is_resistance(self):
        """Check if the response indicates drug resistance."""
        return self.response_type in ['resistance', 'reduced_sensitivity']
    
    def is_high_evidence(self):
        """Check if the evidence level is high (A or B)."""
        return self.evidence_level in ['A', 'B']


class COSMICData(models.Model):
    """
    COSMIC database information.
    
    This model stores cancer mutation data from the COSMIC database,
    including mutation details, cancer types, and frequency information.
    """
    
    # =============================================================================
    # CHOICES
    # =============================================================================
    
    TUMOUR_ORIGIN_CHOICES = [
        ('primary', 'Primary'),
        ('metastasis', 'Metastasis'),
        ('recurrence', 'Recurrence'),
        ('cell_line', 'Cell Line'),
    ]
    
    # =============================================================================
    # BASIC INFORMATION
    # =============================================================================
    
    variant = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name='cosmic_data',
        help_text="Associated genetic variant"
    )
    cosmic_id = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="COSMIC mutation ID"
    )
    
    # =============================================================================
    # MUTATION DETAILS
    # =============================================================================
    
    mutation_description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the mutation"
    )
    mutation_cds = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="CDS mutation notation"
    )
    mutation_aa = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        help_text="Amino acid mutation notation"
    )
    
    # =============================================================================
    # CANCER INFORMATION
    # =============================================================================
    
    primary_site = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Primary cancer site"
    )
    site_subtype = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Cancer site subtype"
    )
    primary_histology = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Primary histology"
    )
    histology_subtype = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Histology subtype"
    )
    
    # =============================================================================
    # SAMPLE INFORMATION
    # =============================================================================
    
    sample_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Sample identifier"
    )
    sample_source = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Sample source"
    )
    tumour_origin = models.CharField(
        max_length=50,
        choices=TUMOUR_ORIGIN_CHOICES,
        null=True,
        blank=True,
        help_text="Tumour origin type"
    )
    
    # =============================================================================
    # FREQUENCY DATA
    # =============================================================================
    
    mutation_frequency = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Mutation frequency"
    )
    mutation_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Number of samples with this mutation"
    )
    
    # =============================================================================
    # ADDITIONAL DATA
    # =============================================================================
    
    cosmic_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Additional COSMIC data as JSON"
    )
    
    # =============================================================================
    # TIMESTAMPS
    # =============================================================================
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['cosmic_id']
        verbose_name = "COSMIC Data"
        verbose_name_plural = "COSMIC Data Records"
    
    def __str__(self):
        return f"{self.cosmic_id} - {self.primary_site or 'Unknown Site'}"
    
    def is_primary_tumour(self):
        """Check if this is from a primary tumour."""
        return self.tumour_origin == 'primary'
    
    def is_metastasis(self):
        """Check if this is from a metastasis."""
        return self.tumour_origin == 'metastasis'


class VariantAnnotation(models.Model):
    """
    Combined annotation data for a variant.
    
    This model stores aggregated annotation information from multiple sources,
    providing a unified view of variant significance and clinical relevance.
    """
    
    # =============================================================================
    # BASIC INFORMATION
    # =============================================================================
    
    variant = models.OneToOneField(
        Variant,
        on_delete=models.CASCADE,
        related_name='annotation',
        help_text="Associated genetic variant"
    )
    
    # =============================================================================
    # SUMMARY FIELDS
    # =============================================================================
    
    is_pathogenic = models.BooleanField(
        default=False,
        help_text="Whether the variant is classified as pathogenic"
    )
    is_drug_target = models.BooleanField(
        default=False,
        help_text="Whether the variant is associated with drug responses"
    )
    has_cosmic_data = models.BooleanField(
        default=False,
        help_text="Whether COSMIC data is available for this variant"
    )
    
    # =============================================================================
    # RISK SCORES
    # =============================================================================
    
    pathogenicity_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Pathogenicity score (0-1)"
    )
    drug_response_score = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        help_text="Drug response score (0-1)"
    )
    
    # =============================================================================
    # ANNOTATION METADATA
    # =============================================================================
    
    annotation_date = models.DateTimeField(
        auto_now=True,
        help_text="Date of last annotation update"
    )
    annotation_version = models.CharField(
        max_length=20,
        default='1.0',
        help_text="Version of annotation pipeline"
    )
    
    # =============================================================================
    # COMBINED ANNOTATION DATA
    # =============================================================================
    
    annotation_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Combined annotation data from all sources"
    )
    
    class Meta:
        ordering = ['-annotation_date']
        verbose_name = "Variant Annotation"
        verbose_name_plural = "Variant Annotations"
    
    def __str__(self):
        return f"Annotation for {self.variant}"
    
    def is_high_confidence(self):
        """Check if the annotation has high confidence scores."""
        return (
            self.pathogenicity_score is not None and self.pathogenicity_score > 0.8
        ) or (
            self.drug_response_score is not None and self.drug_response_score > 0.8
        )
    
    def get_annotation_summary(self):
        """Return a summary of the annotation status."""
        summary = []
        if self.is_pathogenic:
            summary.append("Pathogenic")
        if self.is_drug_target:
            summary.append("Drug Target")
        if self.has_cosmic_data:
            summary.append("COSMIC Data")
        return ", ".join(summary) if summary else "No significant annotations"