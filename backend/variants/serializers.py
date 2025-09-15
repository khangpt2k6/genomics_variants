from rest_framework import serializers
from .models import (
    Variant, ClinicalSignificance, DrugResponse, COSMICData, VariantAnnotation
)


class VariantSerializer(serializers.ModelSerializer):
    """Serializer for Variant model"""
    
    class Meta:
        model = Variant
        fields = [
            'id', 'chromosome', 'position', 'reference_allele', 'alternate_allele',
            'variant_id', 'quality_score', 'filter_status', 'gene_symbol',
            'transcript_id', 'hgvs_c', 'hgvs_p', 'consequence', 'impact',
            'gnomad_af', 'gnomad_af_afr', 'gnomad_af_amr', 'gnomad_af_eas',
            'gnomad_af_nfe', 'gnomad_af_sas', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VariantDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Variant model with related data"""
    
    clinical_significance = serializers.SerializerMethodField()
    drug_responses = serializers.SerializerMethodField()
    cosmic_data = serializers.SerializerMethodField()
    annotations = serializers.SerializerMethodField()
    
    class Meta:
        model = Variant
        fields = [
            'id', 'chromosome', 'position', 'reference_allele', 'alternate_allele',
            'variant_id', 'quality_score', 'filter_status', 'gene_symbol',
            'transcript_id', 'hgvs_c', 'hgvs_p', 'consequence', 'impact',
            'gnomad_af', 'gnomad_af_afr', 'gnomad_af_amr', 'gnomad_af_eas',
            'gnomad_af_nfe', 'gnomad_af_sas', 'vcf_data', 'created_at', 'updated_at',
            'clinical_significance', 'drug_responses', 'cosmic_data', 'annotations'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_clinical_significance(self, obj):
        return ClinicalSignificanceSerializer(obj.clinical_significance.all(), many=True).data
    
    def get_drug_responses(self, obj):
        return DrugResponseSerializer(obj.drug_responses.all(), many=True).data
    
    def get_cosmic_data(self, obj):
        return COSMICDataSerializer(obj.cosmic_data.all(), many=True).data
    
    def get_annotations(self, obj):
        return VariantAnnotationSerializer(obj.annotations.all(), many=True).data


class ClinicalSignificanceSerializer(serializers.ModelSerializer):
    """Serializer for ClinicalSignificance model"""
    
    variant_id = serializers.IntegerField(source='variant.id', read_only=True)
    variant_display = serializers.CharField(source='variant.__str__', read_only=True)
    
    class Meta:
        model = ClinicalSignificance
        fields = [
            'id', 'variant_id', 'variant_display', 'significance', 'review_status',
            'review_date', 'clinvar_id', 'evidence_level', 'phenotype',
            'inheritance_pattern', 'clinvar_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DrugResponseSerializer(serializers.ModelSerializer):
    """Serializer for DrugResponse model"""
    
    variant_id = serializers.IntegerField(source='variant.id', read_only=True)
    variant_display = serializers.CharField(source='variant.__str__', read_only=True)
    
    class Meta:
        model = DrugResponse
        fields = [
            'id', 'variant_id', 'variant_display', 'drug_name', 'response_type',
            'evidence_level', 'evidence_direction', 'civic_id', 'evidence_id',
            'cancer_type', 'tissue_type', 'civic_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class COSMICDataSerializer(serializers.ModelSerializer):
    """Serializer for COSMICData model"""
    
    variant_id = serializers.IntegerField(source='variant.id', read_only=True)
    variant_display = serializers.CharField(source='variant.__str__', read_only=True)
    
    class Meta:
        model = COSMICData
        fields = [
            'id', 'variant_id', 'variant_display', 'cosmic_id', 'mutation_description',
            'mutation_cds', 'mutation_aa', 'primary_site', 'site_subtype',
            'primary_histology', 'histology_subtype', 'sample_name', 'sample_source',
            'tumour_origin', 'mutation_frequency', 'mutation_count', 'cosmic_data',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class VariantAnnotationSerializer(serializers.ModelSerializer):
    """Serializer for VariantAnnotation model"""
    
    variant_id = serializers.IntegerField(source='variant.id', read_only=True)
    variant_display = serializers.CharField(source='variant.__str__', read_only=True)
    
    class Meta:
        model = VariantAnnotation
        fields = [
            'id', 'variant_id', 'variant_display', 'is_pathogenic', 'is_drug_target',
            'has_cosmic_data', 'pathogenicity_score', 'drug_response_score',
            'annotation_date', 'annotation_version', 'annotation_data'
        ]
        read_only_fields = ['id', 'annotation_date']


class VariantCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new variants"""
    
    class Meta:
        model = Variant
        fields = [
            'chromosome', 'position', 'reference_allele', 'alternate_allele',
            'variant_id', 'quality_score', 'filter_status', 'gene_symbol',
            'transcript_id', 'hgvs_c', 'hgvs_p', 'consequence', 'impact',
            'gnomad_af', 'gnomad_af_afr', 'gnomad_af_amr', 'gnomad_af_eas',
            'gnomad_af_nfe', 'gnomad_af_sas', 'vcf_data'
        ]
    
    def validate_variant_id(self, value):
        """Ensure variant_id is unique"""
        if Variant.objects.filter(variant_id=value).exists():
            raise serializers.ValidationError("A variant with this ID already exists.")
        return value
    
    def validate(self, data):
        """Validate variant data"""
        # Check if position is positive
        if data.get('position') and data['position'] <= 0:
            raise serializers.ValidationError("Position must be positive.")
        
        # Check if quality score is within valid range
        quality_score = data.get('quality_score')
        if quality_score is not None and quality_score < 0:
            raise serializers.ValidationError("Quality score must be non-negative.")
        
        return data


class VariantBulkCreateSerializer(serializers.Serializer):
    """Serializer for bulk creating variants from VCF data"""
    
    variants = VariantCreateSerializer(many=True)
    
    def create(self, validated_data):
        variants_data = validated_data['variants']
        variants = []
        
        for variant_data in variants_data:
            variant = Variant.objects.create(**variant_data)
            variants.append(variant)
        
        return {'variants': variants}


class VariantSearchSerializer(serializers.Serializer):
    """Serializer for variant search parameters"""
    
    gene_symbol = serializers.CharField(required=False, allow_blank=True)
    chromosome = serializers.CharField(required=False, allow_blank=True)
    min_position = serializers.IntegerField(required=False, min_value=1)
    max_position = serializers.IntegerField(required=False, min_value=1)
    impact = serializers.ChoiceField(
        choices=['HIGH', 'MODERATE', 'LOW', 'MODIFIER'],
        required=False,
        allow_blank=True
    )
    consequence = serializers.CharField(required=False, allow_blank=True)
    min_gnomad_af = serializers.FloatField(required=False, min_value=0, max_value=1)
    max_gnomad_af = serializers.FloatField(required=False, min_value=0, max_value=1)
    min_quality = serializers.FloatField(required=False, min_value=0)
    
    def validate(self, data):
        """Validate search parameters"""
        min_position = data.get('min_position')
        max_position = data.get('max_position')
        
        if min_position and max_position and min_position > max_position:
            raise serializers.ValidationError("min_position must be less than or equal to max_position.")
        
        min_gnomad_af = data.get('min_gnomad_af')
        max_gnomad_af = data.get('max_gnomad_af')
        
        if min_gnomad_af and max_gnomad_af and min_gnomad_af > max_gnomad_af:
            raise serializers.ValidationError("min_gnomad_af must be less than or equal to max_gnomad_af.")
        
        return data
