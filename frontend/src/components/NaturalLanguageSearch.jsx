import React, { useState } from 'react';
import { geminiService } from '../services/gemini';
import { Search, Sparkles, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function NaturalLanguageSearch() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await geminiService.naturalLanguageSearch(query.trim());
      setResults(data);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Search failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    handleSearch({ preventDefault: () => {} });
  };

  const handleVariantClick = (variantId) => {
    navigate(`/variants/${variantId}`);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-3 mb-4">
        <Sparkles className="text-blue-600" size={24} />
        <h2 className="text-xl font-bold text-gray-900">Natural Language Search</h2>
      </div>

      <form onSubmit={handleSearch} className="mb-4">
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., 'Find all pathogenic variants in BRCA genes'"
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={isLoading}
            />
          </div>
          <button
            type="submit"
            disabled={!query.trim() || isLoading}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            {isLoading ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Searching...
              </>
            ) : (
              <>
                <Search size={18} />
                Search
              </>
            )}
          </button>
        </div>
      </form>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-900 text-sm">{error}</p>
        </div>
      )}

      {results && (
        <div className="space-y-4">
          {results.interpretation && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <p className="text-blue-900 text-sm">
                <strong>Interpretation:</strong> {results.interpretation}
              </p>
            </div>
          )}

          {results.results && results.results.length > 0 ? (
            <div>
              <p className="text-sm text-gray-600 mb-3">
                Found {results.results_count} variant(s)
              </p>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {results.results.map((variant) => (
                  <div
                    key={variant.id}
                    onClick={() => handleVariantClick(variant.id)}
                    className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50 cursor-pointer transition-colors"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <p className="font-semibold text-gray-900">
                          {variant.chromosome}:{variant.position}
                        </p>
                        <p className="text-sm text-gray-600">
                          {variant.reference_allele} &gt; {variant.alternate_allele}
                        </p>
                        {variant.gene_symbol && (
                          <p className="text-sm text-gray-600 mt-1">
                            Gene: {variant.gene_symbol}
                          </p>
                        )}
                      </div>
                      {variant.impact && (
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          variant.impact === 'HIGH' ? 'bg-red-100 text-red-800' :
                          variant.impact === 'MODERATE' ? 'bg-yellow-100 text-yellow-800' :
                          variant.impact === 'LOW' ? 'bg-blue-100 text-blue-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {variant.impact}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <p>No variants found matching your query.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

