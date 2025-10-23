import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import LoadingSpinner from '../components/LoadingSpinner';
import api   from '../services/api';
import { ArrowLeft, AlertCircle, CheckCircle } from 'lucide-react';

export default function VariantDetail() {
  const { id } = useParams();
  const navigate = useNavigate();

  const { data: variant, isLoading, error } = useQuery({
    queryKey: ['variant', id],
    queryFn: async () => {
      const response = await api.get(`/variants/${id}/`);
      return response.data;
    },
  });

  if (isLoading) return <LoadingSpinner />;

  if (error) {
    return (
      <div className="space-y-6">
        <button
          onClick={() => navigate('/variants')}
          className="flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium"
        >
          <ArrowLeft size={20} />
          Back to Variants
        </button>
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 flex items-start gap-3">
          <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={24} />
          <div>
            <h3 className="font-medium text-red-900">Error loading variant</h3>
            <p className="text-red-700 text-sm mt-1">{error.message}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!variant) return null;

  return (
    <div className="space-y-6">
      {/* Back Button */}
      <button
        onClick={() => navigate('/variants')}
        className="flex items-center gap-2 text-primary-600 hover:text-primary-700 font-medium"
      >
        <ArrowLeft size={20} />
        Back to Variants
      </button>

      {/* Header */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {variant.chromosome}:{variant.position}
            </h1>
            <p className="text-gray-600 mt-2">
              {variant.reference_allele} &gt; {variant.alternate_allele}
            </p>
          </div>
          <div className="flex gap-2">
            {variant.impact && (
              <ImpactBadge impact={variant.impact} />
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <InfoCard label="Variant ID" value={variant.variant_id} />
          <InfoCard label="Gene" value={variant.gene_symbol || '-'} />
          <InfoCard label="Consequence" value={variant.consequence || '-'} />
          <InfoCard
            label="Quality Score"
            value={variant.quality_score ? variant.quality_score.toFixed(2) : '-'}
          />
        </div>
      </div>

      {/* Genomic Context */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Genomic Context</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <DetailRow label="Chromosome" value={variant.chromosome} />
          <DetailRow label="Position" value={variant.position} />
          <DetailRow label="Reference Allele" value={variant.reference_allele} />
          <DetailRow label="Alternate Allele" value={variant.alternate_allele} />
          <DetailRow label="Transcript ID" value={variant.transcript_id || '-'} />
          <DetailRow label="HGVS cDNA" value={variant.hgvs_c || '-'} />
          <DetailRow label="HGVS Protein" value={variant.hgvs_p || '-'} />
          <DetailRow label="Filter Status" value={variant.filter_status || 'PASS'} />
        </div>
      </div>

      {/* Functional Impact */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Functional Impact</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <DetailRow label="Impact" value={variant.impact || '-'} />
          <DetailRow label="Consequence" value={variant.consequence || '-'} />
        </div>
      </div>

      {/* Population Frequencies */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          Population Frequencies (gnomAD)
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FrequencyRow
            label="Global AF"
            value={variant.gnomad_af}
          />
          <FrequencyRow
            label="African/African American AF"
            value={variant.gnomad_af_afr}
          />
          <FrequencyRow
            label="Latino/Admixed American AF"
            value={variant.gnomad_af_amr}
          />
          <FrequencyRow
            label="East Asian AF"
            value={variant.gnomad_af_eas}
          />
          <FrequencyRow
            label="Non-Finnish European AF"
            value={variant.gnomad_af_nfe}
          />
          <FrequencyRow
            label="South Asian AF"
            value={variant.gnomad_af_sas}
          />
        </div>
      </div>

      {/* Clinical Significance */}
      {variant.clinical_significance && variant.clinical_significance.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Clinical Significance
          </h2>
          <div className="space-y-4">
            {variant.clinical_significance.map((cs, idx) => (
              <ClinicalSignificanceCard key={idx} data={cs} />
            ))}
          </div>
        </div>
      )}

      {/* Drug Responses */}
      {variant.drug_responses && variant.drug_responses.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Drug Responses
          </h2>
          <div className="space-y-4">
            {variant.drug_responses.map((dr, idx) => (
              <DrugResponseCard key={idx} data={dr} />
            ))}
          </div>
        </div>
      )}

      {/* VCF Data */}
      {variant.vcf_data && Object.keys(variant.vcf_data).length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">VCF Data</h2>
          <div className="bg-gray-50 rounded-lg p-4 overflow-auto">
            <pre className="text-sm text-gray-600 font-mono">
              {JSON.stringify(variant.vcf_data, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

function InfoCard({ label, value }) {
  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">
        {label}
      </p>
      <p className="text-sm font-medium text-gray-900 mt-2 break-all">{value}</p>
    </div>
  );
}

function DetailRow({ label, value }) {
  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">
        {label}
      </p>
      <p className="text-sm font-medium text-gray-900 mt-2 break-all">{value}</p>
    </div>
  );
}

function FrequencyRow({ label, value }) {
  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">
        {label}
      </p>
      <p className="text-sm font-medium text-gray-900 mt-2">
        {value ? (value * 100).toFixed(4) + '%' : '-'}
      </p>
    </div>
  );
}

function ImpactBadge({ impact }) {
  const colors = {
    HIGH: 'bg-red-100 text-red-800',
    MODERATE: 'bg-yellow-100 text-yellow-800',
    LOW: 'bg-blue-100 text-blue-800',
    MODIFIER: 'bg-gray-100 text-gray-800',
  };

  return (
    <span
      className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
        colors[impact] || 'bg-gray-100 text-gray-800'
      }`}
    >
      {impact}
    </span>
  );
}

function ClinicalSignificanceCard({ data }) {
  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-gray-900">{data.significance}</h3>
        {data.is_pathogenic && (
          <div className="flex items-center gap-1 px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-semibold">
            <AlertCircle size={14} />
            Pathogenic
          </div>
        )}
      </div>
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div>
          <p className="text-gray-600">Review Status</p>
          <p className="font-medium text-gray-900">{data.review_status || '-'}</p>
        </div>
        <div>
          <p className="text-gray-600">ClinVar ID</p>
          <p className="font-medium text-gray-900">{data.clinvar_id || '-'}</p>
        </div>
      </div>
      {data.phenotype && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <p className="text-sm text-gray-600">
            <strong>Phenotype:</strong> {data.phenotype}
          </p>
        </div>
      )}
    </div>
  );
}

function DrugResponseCard({ data }) {
  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <div className="flex items-start justify-between mb-3">
        <h3 className="font-semibold text-gray-900">{data.drug_name}</h3>
        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
          data.response_type === 'sensitivity'
            ? 'bg-green-100 text-green-700'
            : 'bg-red-100 text-red-700'
        }`}>
          {data.response_type}
        </span>
      </div>
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div>
          <p className="text-gray-600">Evidence Level</p>
          <p className="font-medium text-gray-900">{data.evidence_level}</p>
        </div>
        <div>
          <p className="text-gray-600">Cancer Type</p>
          <p className="font-medium text-gray-900">{data.cancer_type || '-'}</p>
        </div>
      </div>
    </div>
  );
}
