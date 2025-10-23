import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import ForceDirectedGraph from '../components/ForceDirectedGraph';
import LoadingSpinner from '../components/LoadingSpinner';
import api  from '../services/api';
import { AlertCircle, RefreshCw } from 'lucide-react';

export default function VariantNetwork() {
  const [graphData, setGraphData] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);

  // Fetch variants data
  const { data: variantsData, isLoading, error, refetch } = useQuery({
    queryKey: ['variants-network'],
    queryFn: async () => {
      const response = await api.get('/variants/');
      return response.data;
    },
  });

  // Transform variants data into graph format
  useEffect(() => {
    if (variantsData?.results) {
      const variants = variantsData.results;
      
      // Create nodes from variants and genes
      const nodeMap = new Map();
      const nodes = [];
      const links = [];

      // Add variant nodes
      variants.forEach((variant, idx) => {
        const variantId = `var-${variant.id}`;
        nodeMap.set(variantId, {
          id: variantId,
          label: `${variant.chromosome}:${variant.position}`,
          type: 'variant',
          color: getImpactColor(variant.impact),
          size: 10,
          description: `${variant.reference_allele}>${variant.alternate_allele}`,
        });
        nodes.push(nodeMap.get(variantId));

        // Add gene node if exists
        if (variant.gene_symbol) {
          const geneId = `gene-${variant.gene_symbol}`;
          if (!nodeMap.has(geneId)) {
            nodeMap.set(geneId, {
              id: geneId,
              label: variant.gene_symbol,
              type: 'gene',
              color: '#8b5cf6',
              size: 12,
              description: `Gene: ${variant.gene_symbol}`,
            });
            nodes.push(nodeMap.get(geneId));
          }

          // Create link between variant and gene
          links.push({
            source: variantId,
            target: geneId,
            type: 'variant-gene',
          });
        }
      });

      // Add co-occurrence links between variants with same gene
      const geneVariants = new Map();
      variants.forEach((variant) => {
        if (variant.gene_symbol) {
          if (!geneVariants.has(variant.gene_symbol)) {
            geneVariants.set(variant.gene_symbol, []);
          }
          geneVariants.get(variant.gene_symbol).push(`var-${variant.id}`);
        }
      });

      // Create links between co-occurring variants
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

      setGraphData({ nodes, links });
    }
  }, [variantsData]);

  if (isLoading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Variant Network</h1>
          <p className="text-gray-600 mt-1">
            Visualize relationships between genes and variants
          </p>
        </div>
        <button
          onClick={() => refetch()}
          className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          <RefreshCw size={18} />
          Refresh
        </button>
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
          <div>
            <h3 className="font-medium text-red-900">Error loading data</h3>
            <p className="text-red-700 text-sm mt-1">{error.message}</p>
          </div>
        </div>
      )}

      {/* Graph Container */}
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="p-4 border-b border-gray-200">
          <h2 className="font-semibold text-gray-900">
            Gene-Variant Interaction Network
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            Drag nodes to explore relationships. Hover for details.
          </p>
        </div>
        
        <div className="overflow-x-auto">
          {graphData && (
            <ForceDirectedGraph
              data={graphData}
              width={1000}
              height={600}
            />
          )}
        </div>
      </div>

      {/* Legend */}
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

      {/* Statistics */}
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
