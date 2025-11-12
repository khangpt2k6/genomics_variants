import React, { useState, useEffect } from 'react';
import { Sparkles, Loader2, AlertCircle, Download, RefreshCw } from 'lucide-react';
import { aiApi } from '../services/ai';
import Plot from 'react-plotly.js';

export default function AIGraphGeneration() {
  const [dataInput, setDataInput] = useState('');
  const [graphType, setGraphType] = useState('auto');
  const [loading, setLoading] = useState(false);
  const [graphs, setGraphs] = useState(null);
  const [error, setError] = useState(null);
  const [useVariantData, setUseVariantData] = useState(true);
  const [variantGraphs, setVariantGraphs] = useState(null);

  useEffect(() => {
    if (useVariantData) {
      loadVariantStatisticsGraph();
    }
  }, [useVariantData]);

  const loadVariantStatisticsGraph = async () => {
    try {
      setLoading(true);
      const result = await aiApi.getVariantStatisticsGraph();
      setVariantGraphs(result);
    } catch (err) {
      console.error('Failed to load variant statistics graph:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (!dataInput.trim()) {
      setError('Please provide data');
      return;
    }

    setLoading(true);
    setError(null);
    setGraphs(null);

    try {
      let data;
      try {
        data = JSON.parse(dataInput);
      } catch (e) {
        throw new Error('Invalid JSON format. Please provide valid JSON data.');
      }

      const result = await aiApi.generateGraph(data, graphType);
      setGraphs(result);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Failed to generate graph');
      console.error('Graph generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadExampleData = () => {
    const example = {
      genes: ['BRCA1', 'BRCA2', 'TP53', 'EGFR', 'KRAS'],
      counts: [150, 120, 100, 80, 60],
      impacts: ['HIGH', 'MODERATE', 'LOW', 'MODIFIER'],
      impact_counts: [50, 100, 200, 150]
    };
    setDataInput(JSON.stringify(example, null, 2));
  };

  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <div className="mb-8">
          <h1 className="text-5xl font-bold text-black mb-3 tracking-tight">
            AI Graph Generation
          </h1>
          <p className="text-gray-600">
            Generate intelligent visualizations from your data using AI
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg">
              <h2 className="text-xl font-semibold text-black mb-4 flex items-center gap-2">
                <Sparkles size={24} />
                Generate Custom Graph
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Graph Type
                  </label>
                  <select
                    value={graphType}
                    onChange={(e) => setGraphType(e.target.value)}
                    className="w-full px-4 py-2 border border-black/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-black/20"
                  >
                    <option value="auto">Auto (AI Recommended)</option>
                    <option value="bar">Bar Chart</option>
                    <option value="line">Line Chart</option>
                    <option value="pie">Pie Chart</option>
                    <option value="scatter">Scatter Plot</option>
                    <option value="heatmap">Heatmap</option>
                  </select>
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-gray-700">
                      Data (JSON Format)
                    </label>
                    <button
                      onClick={loadExampleData}
                      className="text-xs text-gray-600 hover:text-black underline"
                    >
                      Load Example
                    </button>
                  </div>
                  <textarea
                    value={dataInput}
                    onChange={(e) => setDataInput(e.target.value)}
                    rows={10}
                    className="w-full px-4 py-2 border border-black/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-black/20 font-mono text-sm"
                    placeholder='{"labels": ["A", "B", "C"], "values": [10, 20, 30]}'
                  />
                </div>

                <button
                  onClick={handleGenerate}
                  disabled={loading || !dataInput.trim()}
                  className="w-full px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="animate-spin" size={20} />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Sparkles size={20} />
                      Generate Graph
                    </>
                  )}
                </button>
              </div>
            </div>

            {error && (
              <div className="backdrop-blur-xl bg-red-50 border border-red-200 rounded-2xl p-6 shadow-lg">
                <div className="flex items-start gap-3">
                  <AlertCircle className="text-red-600 flex-shrink-0 mt-0.5" size={20} />
                  <div>
                    <h3 className="font-semibold text-red-900 mb-1">Error</h3>
                    <p className="text-red-700">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {graphs && (
              <div className="space-y-6">
                {Object.entries(graphs.graphs || {}).map(([graphType, graphData]) => (
                  <div
                    key={graphType}
                    className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg"
                  >
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-black capitalize">
                        {graphType} Chart
                      </h3>
                    </div>

                    {graphData.error ? (
                      <p className="text-red-600">{graphData.error}</p>
                    ) : (
                      <Plot
                        data={graphData.data?.data || []}
                        layout={{
                          ...graphData.data?.layout,
                          autosize: true,
                          height: 400
                        }}
                        style={{ width: '100%', height: '400px' }}
                        config={{ responsive: true }}
                      />
                    )}

                    {graphData.description && (
                      <p className="text-sm text-gray-600 mt-4">{graphData.description}</p>
                    )}
                  </div>
                ))}

                {graphs.recommendations && graphs.recommendations.length > 0 && (
                  <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg">
                    <h3 className="text-lg font-semibold text-black mb-3">AI Recommendations</h3>
                    <ul className="list-disc list-inside space-y-2 text-gray-700">
                      {graphs.recommendations.map((rec, idx) => (
                        <li key={idx}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {useVariantData && variantGraphs && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold text-black">Variant Statistics Graphs</h2>
                  <button
                    onClick={loadVariantStatisticsGraph}
                    className="flex items-center gap-2 px-4 py-2 bg-black/10 hover:bg-black/20 rounded-lg transition-colors"
                  >
                    <RefreshCw size={16} />
                    Refresh
                  </button>
                </div>

                {Object.entries(variantGraphs.graphs || {}).map(([graphType, graphData]) => (
                  <div
                    key={graphType}
                    className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg"
                  >
                    <h3 className="text-lg font-semibold text-black mb-4 capitalize">
                      {graphType} Chart
                    </h3>

                    {graphData.error ? (
                      <p className="text-red-600">{graphData.error}</p>
                    ) : (
                      <Plot
                        data={graphData.data?.data || []}
                        layout={{
                          ...graphData.data?.layout,
                          autosize: true,
                          height: 400
                        }}
                        style={{ width: '100%', height: '400px' }}
                        config={{ responsive: true }}
                      />
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg">
              <h2 className="text-xl font-semibold text-black mb-4">Options</h2>

              <div className="space-y-4">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={useVariantData}
                    onChange={(e) => setUseVariantData(e.target.checked)}
                    className="w-4 h-4 text-black border-black/20 rounded focus:ring-black/20"
                  />
                  <span className="text-sm text-gray-700">Show Variant Statistics</span>
                </label>
              </div>
            </div>

            <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg">
              <h2 className="text-xl font-semibold text-black mb-4">Data Format</h2>
              <p className="text-sm text-gray-600 mb-3">
                Provide data in JSON format. Examples:
              </p>
              <pre className="text-xs bg-white/50 p-3 rounded overflow-x-auto">
{`{
  "labels": ["A", "B", "C"],
  "values": [10, 20, 30]
}`}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

