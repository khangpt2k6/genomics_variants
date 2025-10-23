import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';
import  api  from '../services/api';
import { Search, Filter, ChevronRight, AlertCircle } from 'lucide-react';

export default function Variants() {
  const [searchTerm, setSearchTerm] = useState('');
  const [impactFilter, setImpactFilter] = useState('');
  const [page, setPage] = useState(1);

  const { data, isLoading, error } = useQuery({
    queryKey: ['variants', page, searchTerm, impactFilter],
    queryFn: async () => {
      let url = `/variants/?page=${page}`;
      if (searchTerm) url += `&search=${searchTerm}`;
      if (impactFilter) url += `&impact=${impactFilter}`;
      const response = await api.get(url);
      return response.data;
    },
  });

  if (isLoading) return <LoadingSpinner />;

  const variants = data?.results || [];
  const totalPages = data?.count ? Math.ceil(data.count / 20) : 1;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Variants</h1>
        <p className="text-gray-600 mt-1">Browse and filter genetic variants</p>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="text"
              placeholder="Search variants..."
              value={searchTerm}
              onChange={(e) => {
                setSearchTerm(e.target.value);
                setPage(1);
              }}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          {/* Impact Filter */}
          <select
            value={impactFilter}
            onChange={(e) => {
              setImpactFilter(e.target.value);
              setPage(1);
            }}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="">All Impact Levels</option>
            <option value="HIGH">High</option>
            <option value="MODERATE">Moderate</option>
            <option value="LOW">Low</option>
            <option value="MODIFIER">Modifier</option>
          </select>

          {/* Results Count */}
          <div className="flex items-center justify-end">
            <p className="text-gray-600">
              {data?.count || 0} variants found
            </p>
          </div>
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
          <div>
            <h3 className="font-medium text-red-900">Error loading variants</h3>
            <p className="text-red-700 text-sm mt-1">{error.message}</p>
          </div>
        </div>
      )}

      {/* Variants Table */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                  Variant
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                  Gene
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                  Impact
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                  Consequence
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-gray-900">
                  gnomAD AF
                </th>
                <th className="px-6 py-3 text-right text-sm font-semibold text-gray-900">
                  Action
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {variants.length > 0 ? (
                variants.map((variant) => (
                  <tr
                    key={variant.id}
                    className="hover:bg-gray-50 transition-colors"
                  >
                    <td className="px-6 py-4">
                      <div className="font-mono text-sm font-medium text-gray-900">
                        {variant.chromosome}:{variant.position}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">
                        {variant.reference_allele} &gt; {variant.alternate_allele}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm font-medium text-gray-900">
                        {variant.gene_symbol || '-'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <ImpactBadge impact={variant.impact} />
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-600">
                        {variant.consequence || '-'}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-600">
                        {variant.gnomad_af
                          ? (variant.gnomad_af * 100).toFixed(3) + '%'
                          : '-'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link
                        to={`/variants/${variant.id}`}
                        className="inline-flex items-center gap-1 text-primary-600 hover:text-primary-700 font-medium"
                      >
                        View
                        <ChevronRight size={16} />
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="6" className="px-6 py-8 text-center">
                    <p className="text-gray-500">No variants found</p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="text-gray-600">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
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
      className={`inline-block px-3 py-1 rounded-full text-xs font-semibold ${
        colors[impact] || 'bg-gray-100 text-gray-800'
      }`}
    >
      {impact || 'Unknown'}
    </span>
  );
}
