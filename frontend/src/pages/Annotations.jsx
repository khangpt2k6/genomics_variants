import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import LoadingSpinner from '../components/LoadingSpinner';
import api from '../services/api';
import { AlertCircle, CheckCircle, AlertTriangle, Info } from 'lucide-react';

export default function Annotations() {
  const [selectedVariant, setSelectedVariant] = useState(null);

  const { data: annotationsData, isLoading, error } = useQuery({
    queryKey: ['annotations'],
    queryFn: async () => {
      const response = await api.get('/annotations/');
      return response.data;
    },
  });

  if (isLoading) return <LoadingSpinner />;

  const annotations = annotationsData?.results || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Annotations</h1>
        <p className="text-gray-600 mt-1">
          View detailed variant annotations from ClinVar and CIViC
        </p>
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
          <div>
            <h3 className="font-medium text-red-900">Error loading annotations</h3>
            <p className="text-red-700 text-sm mt-1">{error.message}</p>
          </div>
        </div>
      )}

      {/* Annotations Grid */}
      <div className="grid grid-cols-1 gap-6">
        {annotations.length > 0 ? (
          annotations.map((annotation) => (
            <AnnotationCard
              key={annotation.id}
              annotation={annotation}
              isSelected={selectedVariant?.id === annotation.id}
              onSelect={() => setSelectedVariant(annotation)}
            />
          ))
        ) : (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <Info className="mx-auto text-gray-400 mb-4" size={48} />
            <p className="text-gray-500 text-lg">No annotations available</p>
          </div>
        )}
      </div>

      {/* Selected Annotation Details */}
      {selectedVariant && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Detailed Annotation
          </h2>
          <AnnotationDetails annotation={selectedVariant} />
        </div>
      )}
    </div>
  );
}

function AnnotationCard({ annotation, isSelected, onSelect }) {
  const variant = annotation.variant;

  return (
    <div
      onClick={onSelect}
      className={`bg-white rounded-lg shadow-md p-6 cursor-pointer transition-all border-2 ${
        isSelected
          ? 'border-primary-500 bg-primary-50'
          : 'border-transparent hover:shadow-lg'
      }`}
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            {variant.chromosome}:{variant.position}
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            {variant.reference_allele} &gt; {variant.alternate_allele}
          </p>
        </div>
        <div className="flex gap-2">
          {annotation.is_pathogenic && (
            <PathogenicBadge />
          )}
          {annotation.is_drug_target && (
            <DrugTargetBadge />
          )}
          {annotation.has_cosmic_data && (
            <CosmicBadge />
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <InfoItem label="Gene" value={variant.gene_symbol || '-'} />
        <InfoItem label="Impact" value={variant.impact || '-'} />
        <InfoItem label="Consequence" value={variant.consequence || '-'} />
        <InfoItem
          label="gnomAD AF"
          value={
            variant.gnomad_af
              ? (variant.gnomad_af * 100).toFixed(3) + '%'
              : '-'
          }
        />
      </div>

      {annotation.annotation_data && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <p className="text-sm text-gray-600">
            <strong>Summary:</strong> {annotation.get_annotation_summary?.()}
          </p>
        </div>
      )}
    </div>
  );
}

function AnnotationDetails({ annotation }) {
  const variant = annotation.variant;

  return (
    <div className="space-y-6">
      {/* Basic Information */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-3">Basic Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <DetailRow label="Chromosome" value={variant.chromosome} />
          <DetailRow label="Position" value={variant.position} />
          <DetailRow label="Reference Allele" value={variant.reference_allele} />
          <DetailRow label="Alternate Allele" value={variant.alternate_allele} />
          <DetailRow label="Gene Symbol" value={variant.gene_symbol || '-'} />
          <DetailRow label="Transcript ID" value={variant.transcript_id || '-'} />
        </div>
      </div>

      {/* Functional Impact */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-3">Functional Impact</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <DetailRow label="Impact" value={variant.impact || '-'} />
          <DetailRow label="Consequence" value={variant.consequence || '-'} />
          <DetailRow label="HGVS cDNA" value={variant.hgvs_c || '-'} />
          <DetailRow label="HGVS Protein" value={variant.hgvs_p || '-'} />
        </div>
      </div>

      {/* Population Frequencies */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-3">Population Frequencies</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <DetailRow
            label="gnomAD Global AF"
            value={
              variant.gnomad_af
                ? (variant.gnomad_af * 100).toFixed(4) + '%'
                : '-'
            }
          />
          <DetailRow
            label="gnomAD AFR AF"
            value={
              variant.gnomad_af_afr
                ? (variant.gnomad_af_afr * 100).toFixed(4) + '%'
                : '-'
            }
          />
          <DetailRow
            label="gnomAD EAS AF"
            value={
              variant.gnomad_af_eas
                ? (variant.gnomad_af_eas * 100).toFixed(4) + '%'
                : '-'
            }
          />
          <DetailRow
            label="gnomAD NFE AF"
            value={
              variant.gnomad_af_nfe
                ? (variant.gnomad_af_nfe * 100).toFixed(4) + '%'
                : '-'
            }
          />
        </div>
      </div>

      {/* Annotation Scores */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-3">Annotation Scores</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <DetailRow
            label="Pathogenicity Score"
            value={
              annotation.pathogenicity_score
                ? (annotation.pathogenicity_score * 100).toFixed(1) + '%'
                : '-'
            }
          />
          <DetailRow
            label="Drug Response Score"
            value={
              annotation.drug_response_score
                ? (annotation.drug_response_score * 100).toFixed(1) + '%'
                : '-'
            }
          />
        </div>
      </div>
    </div>
  );
}

function DetailRow({ label, value }) {
  return (
    <div className="bg-gray-50 rounded-lg p-3">
      <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">
        {label}
      </p>
      <p className="text-sm font-medium text-gray-900 mt-1 break-all">{value}</p>
    </div>
  );
}

function InfoItem({ label, value }) {
  return (
    <div>
      <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">
        {label}
      </p>
      <p className="text-sm font-medium text-gray-900 mt-1">{value}</p>
    </div>
  );
}

function PathogenicBadge() {
  return (
    <div className="flex items-center gap-1 px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-semibold">
      <AlertTriangle size={14} />
      Pathogenic
    </div>
  );
}

function DrugTargetBadge() {
  return (
    <div className="flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold">
      <CheckCircle size={14} />
      Drug Target
    </div>
  );
}

function CosmicBadge() {
  return (
    <div className="flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold">
      <Info size={14} />
      COSMIC
    </div>
  );
}
