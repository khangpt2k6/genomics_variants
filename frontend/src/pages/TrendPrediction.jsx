import React, { useState, useEffect } from 'react';
import { TrendingUp, Calendar, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import { aiApi } from '../services/ai';
import Plot from 'react-plotly.js';

export default function TrendPrediction() {
  const [daysAhead, setDaysAhead] = useState(30);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [recentPredictions, setRecentPredictions] = useState([]);

  useEffect(() => {
    loadRecentPredictions();
  }, []);

  const loadRecentPredictions = async () => {
    try {
      const data = await aiApi.getTrendPredictions();
      setRecentPredictions(data.predictions || []);
    } catch (err) {
      console.error('Failed to load recent predictions:', err);
    }
  };

  const handlePredict = async () => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const result = await aiApi.predictTrends(daysAhead);
      setPrediction(result);
      loadRecentPredictions();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate prediction');
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getTrendColor = (direction) => {
    switch (direction) {
      case 'increasing':
        return 'text-red-600';
      case 'decreasing':
        return 'text-green-600';
      case 'stable':
        return 'text-gray-600';
      default:
        return 'text-gray-600';
    }
  };

  const getTrendIcon = (direction) => {
    switch (direction) {
      case 'increasing':
        return <TrendingUp className="text-red-600" size={20} />;
      case 'decreasing':
        return <TrendingUp className="text-green-600 rotate-180" size={20} />;
      default:
        return <Calendar className="text-gray-600" size={20} />;
    }
  };

  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        <div className="mb-8">
          <h1 className="text-5xl font-bold text-black mb-3 tracking-tight">
            AI Trend Prediction
          </h1>
          <p className="text-gray-600">
            Predict future cancer variant discovery trends using AI-powered analysis
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg">
              <h2 className="text-xl font-semibold text-black mb-4 flex items-center gap-2">
                <TrendingUp size={24} />
                Generate Prediction
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Prediction Horizon (days)
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="365"
                    value={daysAhead}
                    onChange={(e) => setDaysAhead(parseInt(e.target.value) || 30)}
                    className="w-full px-4 py-2 border border-black/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-black/20"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Predict variant trends for the next {daysAhead} days
                  </p>
                </div>

                <button
                  onClick={handlePredict}
                  disabled={loading}
                  className="w-full px-6 py-3 bg-black text-white rounded-lg hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {loading ? (
                    <>
                      <Loader2 className="animate-spin" size={20} />
                      Generating Prediction...
                    </>
                  ) : (
                    <>
                      <TrendingUp size={20} />
                      Generate Prediction
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

            {prediction && (
              <div className="space-y-6">
                <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg">
                  <h2 className="text-xl font-semibold text-black mb-4">Prediction Results</h2>

                  <div className="grid grid-cols-2 gap-4 mb-6">
                    <div className="bg-white/50 rounded-lg p-4">
                      <p className="text-sm text-gray-600 mb-1">Trend Direction</p>
                      <div className="flex items-center gap-2">
                        {getTrendIcon(prediction.predictions?.trend_direction)}
                        <span className={`font-semibold ${getTrendColor(prediction.predictions?.trend_direction)}`}>
                          {prediction.predictions?.trend_direction?.toUpperCase() || 'UNKNOWN'}
                        </span>
                      </div>
                    </div>

                    <div className="bg-white/50 rounded-lg p-4">
                      <p className="text-sm text-gray-600 mb-1">Confidence Score</p>
                      <p className="text-2xl font-bold text-black">
                        {(prediction.confidence_score * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>

                  {prediction.charts?.trend_chart && (
                    <div className="mt-6">
                      <Plot
                        data={prediction.charts.trend_chart.data}
                        layout={{
                          ...prediction.charts.trend_chart.layout,
                          autosize: true,
                          height: 400
                        }}
                        style={{ width: '100%', height: '400px' }}
                        config={{ responsive: true }}
                      />
                    </div>
                  )}
                </div>

                {prediction.analysis && (
                  <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg">
                    <h2 className="text-xl font-semibold text-black mb-4">AI Analysis</h2>

                    {prediction.analysis.key_trends && (
                      <div className="mb-6">
                        <h3 className="font-semibold text-black mb-2">Key Trends</h3>
                        <ul className="list-disc list-inside space-y-1 text-gray-700">
                          {prediction.analysis.key_trends.map((trend, idx) => (
                            <li key={idx}>{trend}</li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {prediction.analysis.significant_genes && prediction.analysis.significant_genes.length > 0 && (
                      <div className="mb-6">
                        <h3 className="font-semibold text-black mb-2">Significant Genes</h3>
                        <div className="flex flex-wrap gap-2">
                          {prediction.analysis.significant_genes.map((gene, idx) => (
                            <span
                              key={idx}
                              className="px-3 py-1 bg-black/10 rounded-full text-sm font-medium text-black"
                            >
                              {gene}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {prediction.analysis.recommendations && (
                      <div>
                        <h3 className="font-semibold text-black mb-2">Recommendations</h3>
                        <ul className="list-disc list-inside space-y-1 text-gray-700">
                          {prediction.analysis.recommendations.map((rec, idx) => (
                            <li key={idx}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>

          <div className="space-y-6">
            <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg">
              <h2 className="text-xl font-semibold text-black mb-4">Recent Predictions</h2>

              {recentPredictions.length === 0 ? (
                <p className="text-gray-500 text-sm">No recent predictions</p>
              ) : (
                <div className="space-y-3">
                  {recentPredictions.map((pred) => (
                    <div
                      key={pred.prediction_id}
                      className="bg-white/50 rounded-lg p-3 border border-black/10"
                    >
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-xs text-gray-500">
                          {new Date(pred.created_at).toLocaleDateString()}
                        </span>
                        <span className={`text-xs font-medium ${getTrendColor(pred.trend_direction)}`}>
                          {pred.trend_direction}
                        </span>
                      </div>
                      <p className="text-sm font-medium text-black">{pred.prediction_id}</p>
                      <p className="text-xs text-gray-600 mt-1">
                        Confidence: {(pred.confidence_score * 100).toFixed(0)}%
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

