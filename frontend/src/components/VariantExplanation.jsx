import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { geminiService } from '../services/gemini';
import LoadingSpinner from './LoadingSpinner';
import { Sparkles, AlertCircle, RefreshCw } from 'lucide-react';

export default function VariantExplanation({ variantId }) {
  const [refetchKey, setRefetchKey] = useState(0);

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['variant-explanation', variantId, refetchKey],
    queryFn: () => geminiService.getVariantExplanation(variantId),
    enabled: !!variantId,
    retry: 1,
  });

  const handleRefresh = () => {
    setRefetchKey(prev => prev + 1);
    refetch();
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center gap-3 mb-4">
          <Sparkles className="text-blue-600" size={24} />
          <h2 className="text-xl font-bold text-gray-900">AI Explanation</h2>
        </div>
        <LoadingSpinner />
        <p className="text-sm text-gray-600 mt-4 text-center">
          Generating AI-powered explanation...
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center gap-3 mb-4">
          <Sparkles className="text-blue-600" size={24} />
          <h2 className="text-xl font-bold text-gray-900">AI Explanation</h2>
        </div>
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
          <div className="flex-1">
            <p className="text-red-900 font-medium">Unable to generate explanation</p>
            <p className="text-red-700 text-sm mt-1">
              {error.response?.data?.error || error.message || 'An error occurred'}
            </p>
            <button
              onClick={handleRefresh}
              className="mt-3 text-sm text-red-700 hover:text-red-900 underline"
            >
              Try again
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!data?.interpretation) {
    return null;
  }

  const interpretation = data.interpretation;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <Sparkles className="text-blue-600" size={24} />
          <h2 className="text-xl font-bold text-gray-900">AI Explanation</h2>
        </div>
        <button
          onClick={handleRefresh}
          className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
          title="Refresh explanation"
        >
          <RefreshCw size={18} />
        </button>
      </div>

      {interpretation.summary && (
        <div className="mb-6">
          <h3 className="font-semibold text-gray-900 mb-2">Summary</h3>
          <p className="text-gray-700 leading-relaxed">{interpretation.summary}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {interpretation.functional_impact && (
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Functional Impact</h3>
            <p className="text-gray-700 text-sm">{interpretation.functional_impact}</p>
          </div>
        )}

        {interpretation.clinical_interpretation && (
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Clinical Interpretation</h3>
            <p className="text-gray-700 text-sm">{interpretation.clinical_interpretation}</p>
          </div>
        )}

        {interpretation.population_context && (
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Population Context</h3>
            <p className="text-gray-700 text-sm">{interpretation.population_context}</p>
          </div>
        )}

        {interpretation.drug_implications && (
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Drug Implications</h3>
            <p className="text-gray-700 text-sm">{interpretation.drug_implications}</p>
          </div>
        )}
      </div>

      {interpretation.key_points && interpretation.key_points.length > 0 && (
        <div className="border-t border-gray-200 pt-4">
          <h3 className="font-semibold text-gray-900 mb-3">Key Points</h3>
          <ul className="space-y-2">
            {interpretation.key_points.map((point, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-blue-600 mt-1">•</span>
                <span className="text-gray-700 text-sm">{point}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {interpretation.confidence_level && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <span className="text-xs text-gray-500">
            Confidence: <span className="font-medium">{interpretation.confidence_level}</span>
          </span>
        </div>
      )}
    </div>
  );
}

