import React, { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import ForceDirectedGraph from './ForceDirectedGraph';
import LoadingSpinner from './LoadingSpinner';
import api from '../services/api';
import { RefreshCw, Sliders } from 'lucide-react';

export default function InteractiveVisualization() {
  const [variantLimit, setVariantLimit] = useState(100);
  const [nodeSize, setNodeSize] = useState(10);
  const [filterImpact, setFilterImpact] = useState('');
  const [geneFilter, setGeneFilter] = useState('');

  const { data: variantsData, isLoading, error, refetch } = useQuery({
    queryKey: ['interactive-visualization', variantLimit],
    queryFn: async () => {
      const response = await api.get(
        `/variants/?page_size=${Math.min(variantLimit, 10000)}&page=1`
      );
      return response.data;
    },
  });

  const graphData = useMemo(() => {
    if (!variantsData?.results) return null;

    let variants = variantsData.results;

    if (filterImpact) {
      variants = variants.filter(v => v.impact === filterImpact);
    }

    if (geneFilter) {
      variants = variants.filter(v =>
        v.gene_symbol?.toLowerCase().includes(geneFilter.toLowerCase())
      );
    }

    const nodeMap = new Map();
    const nodes = [];
    const links = [];

    variants.forEach((variant) => {
      const variantId = `var-${variant.id}`;
      nodeMap.set(variantId, {
        id: variantId,
        label: `${variant.chromosome}:${variant.position}`,
        type: 'variant',
        color: getImpactColor(variant.impact),
        size: nodeSize,
        description: `${variant.reference_allele}>${variant.alternate_allele}`,
      });
      nodes.push(nodeMap.get(variantId));

      if (variant.gene_symbol) {
        const geneId = `gene-${variant.gene_symbol}`;
        if (!nodeMap.has(geneId)) {
          nodeMap.set(geneId, {
            id: geneId,
            label: variant.gene_symbol,
            type: 'gene',
            color: '#8b5cf6',
            size: nodeSize + 2,
            description: `Gene: ${variant.gene_symbol}`,
          });
          nodes.push(nodeMap.get(geneId));
        }

        links.push({
          source: variantId,
          target: geneId,
          type: 'variant-gene',
        });
      }
    });

    const geneVariants = new Map();
    variants.forEach((variant) => {
      if (variant.gene_symbol) {
        if (!geneVariants.has(variant.gene_symbol)) {
          geneVariants.set(variant.gene_symbol, []);
        }
        geneVariants.get(variant.gene_symbol).push(`var-${variant.id}`);
      }
    });

    geneVariants.forEach((variantIds) => {
      for (let i = 0; i < variantIds.length; i++) {
        for (let j = i + 1; j < variantIds.length; j++) {
          links.push({
            source: variantIds[i],
            target: variantIds[j],
            type: 'co-occurrence',
          });
        }
      }
    });

    return { nodes, links };
  }, [variantsData, filterImpact, geneFilter, nodeSize]);

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Interactive Variant Visualization
          </h1>
          <p className="text-gray-600 mt-1">
            Customize your visualization parameters in real-time
          </p>
        </div>
        <button
          onClick={() => refetch()}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          <RefreshCw size={18} />
          Refresh
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center gap-2 mb-4">
          <Sliders size={20} className="text-gray-600" />
          <h2 className="text-xl font-semibold text-gray-900">
            Visualization Controls
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Variants: <span className="font-bold text-blue-600">{variantLimit}</span>
            </label>
            <input
              type="range"
              min="10"
              max="10000"
              step="10"
              value={variantLimit}
              onChange={(e) => setVariantLimit(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>10</span>
              <span>10,000</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Node Size: <span className="font-bold text-blue-600">{nodeSize}px</span>
            </label>
            <input
              type="range"
              min="5"
              max="30"
              step="1"
              value={nodeSize}
              onChange={(e) => setNodeSize(parseInt(e.target.value))}
              className="w-full h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>5px</span>
              <span>30px</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filter by Impact
            </label>
            <select
              value={filterImpact}
              onChange={(e) => setFilterImpact(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Impact Levels</option>
              <option value="HIGH">High</option>
              <option value="MODERATE">Moderate</option>
              <option value="LOW">Low</option>
              <option value="MODIFIER">Modifier</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Filter by Gene
            </label>
            <input
              type="text"
              placeholder="Enter gene name..."
              value={geneFilter}
              onChange={(e) => setGeneFilter(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <span className="text-red-600 font-semibold">Error:</span>
          <p className="text-red-700">{error.message}</p>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-4 border-b border-gray-200">
          <h2 className="font-semibold text-gray-900">
            Gene-Variant Network Visualization
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            Displaying {graphData?.nodes.length || 0} nodes with {graphData?.links.length || 0} connections
          </p>
        </div>

        <div className="overflow-x-auto bg-gray-50">
          {graphData ? (
            <ForceDirectedGraph
              data={graphData}
              width={1000}
              height={600}
            />
          ) : (
            <div className="h-96 flex items-center justify-center text-gray-500">
              No data available
            </div>
          )}
        </div>
      </div>

      {graphData && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm font-medium">Total Nodes</p>
            <p className="text-3xl font-bold text-gray-900 mt-2">
              {graphData.nodes.length}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm font-medium">Total Connections</p>
            <p className="text-3xl font-bold text-gray-900 mt-2">
              {graphData.links.length}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <p className="text-gray-600 text-sm font-medium">Unique Genes</p>
            <p className="text-3xl font-bold text-gray-900 mt-2">
              {graphData.nodes.filter(n => n.type === 'gene').length}
            </p>
          </div>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="font-semibold text-gray-900 mb-4">Legend</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-sm text-gray-600">High Impact</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
            <span className="text-sm text-gray-600">Moderate Impact</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-blue-500"></div>
            <span className="text-sm text-gray-600">Low Impact</span>
          </div>
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 rounded-full bg-purple-500"></div>
            <span className="text-sm text-gray-600">Gene</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function getImpactColor(impact) {
  const colors = {
    'HIGH': '#ef4444',
    'MODERATE': '#eab308',
    'LOW': '#3b82f6',
    'MODIFIER': '#6b7280',
  };
  return colors[impact] || '#0ea5e9';
}
