import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Dna, Network, FileText, TrendingUp, AlertCircle } from 'lucide-react';
import { variantsApi } from '../services/variants';

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalVariants: 0,
    pathogenicVariants: 0,
    impactCounts: { HIGH: 0, MODERATE: 0, LOW: 0, MODIFIER: 0 },
    topGenes: []
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log('Fetching dashboard statistics from API...');

        const statistics = await variantsApi.getStatistics();
        console.log('API response:', statistics);

        // Transform API data to match component expectations
        const transformedStats = {
          totalVariants: statistics.total_variants || 0,
          pathogenicVariants: statistics.pathogenic_variants || 0,
          impactCounts: {
            HIGH: statistics.impact_counts?.HIGH || 0,
            MODERATE: statistics.impact_counts?.MODERATE || 0,
            LOW: statistics.impact_counts?.LOW || 0,
            MODIFIER: statistics.impact_counts?.MODIFIER || 0,
          },
          topGenes: statistics.top_genes?.map(gene => ({
            name: gene.name || gene.gene_symbol,
            count: gene.count || gene.variant_count
          })) || []
        };

        setStats(transformedStats);
        console.log('Transformed stats:', transformedStats);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const impactData = [
    { name: 'HIGH', value: stats.impactCounts.HIGH },
    { name: 'MODERATE', value: stats.impactCounts.MODERATE },
    { name: 'LOW', value: stats.impactCounts.LOW },
    { name: 'MODIFIER', value: stats.impactCounts.MODIFIER },
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-white p-8 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white p-8 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle size={48} className="text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Error Loading Dashboard</h2>
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-5xl font-bold text-black mb-3 tracking-tight">
            Variant Analysis Dashboard
          </h1>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <MetricCard
            icon={Dna}
            label="Total Variants"
            value={stats.totalVariants}
          />
          <MetricCard
            icon={AlertCircle}
            label="Pathogenic"
            value={stats.pathogenicVariants}
          />
          <MetricCard
            icon={TrendingUp}
            label="High Impact"
            value={stats.impactCounts.HIGH}
          />
          <MetricCard
            icon={Network}
            label="Unique Genes"
            value={stats.topGenes.length}
          />
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Impact Distribution */}
          <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-8 shadow-lg">
            <h2 className="text-xl font-semibold text-black mb-6 flex items-center gap-2">
              <div className="w-1 h-6 bg-black rounded-full"></div>
              Variant Impact Distribution
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={impactData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#00000020" />
                <XAxis dataKey="name" stroke="#000" tick={{ fill: '#000' }} />
                <YAxis stroke="#000" tick={{ fill: '#000' }} />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                    border: '1px solid rgba(0, 0, 0, 0.1)',
                    borderRadius: '8px',
                    color: '#000'
                  }}
                />
                <Bar dataKey="value" fill="#000" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Top Genes */}
          <div className="backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-8 shadow-lg">
            <h2 className="text-xl font-semibold text-black mb-6 flex items-center gap-2">
              <div className="w-1 h-6 bg-black rounded-full"></div>
              Top Genes by Variant Count
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={stats.topGenes}
                layout="vertical"
                margin={{ left: 80 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="#00000020" />
                <XAxis type="number" stroke="#000" tick={{ fill: '#000' }} />
                <YAxis 
                  dataKey="name" 
                  type="category" 
                  width={80} 
                  stroke="#000" 
                  tick={{ fill: '#000' }}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                    border: '1px solid rgba(0, 0, 0, 0.1)',
                    borderRadius: '8px',
                    color: '#000'
                  }}
                />
                <Bar dataKey="count" fill="#000" radius={[0, 8, 8, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <QuickActionCard
            icon={Dna}
            title="Browse Variants"
            description="View and filter all genetic variants"
          />
          <QuickActionCard
            icon={Network}
            title="Variant Network"
            description="Explore gene-variant relationships"
          />
          <QuickActionCard
            icon={FileText}
            title="Annotations"
            description="View detailed variant annotations"
          />
        </div>
      </div>
    </div>
  );
}

function MetricCard({ icon: Icon, label, value }) {
  return (
    <div className="group backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-5 shadow-lg hover:bg-black/10 hover:border-black/20 transition-all duration-300 cursor-pointer">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-xs font-medium uppercase tracking-wide">{label}</p>
          <p className="text-3xl font-bold text-black mt-2">{value}</p>
        </div>
        <div className="p-3 rounded-xl bg-black/10 border border-black/20 group-hover:bg-black/20 transition-all">
          <Icon size={24} className="text-black" />
        </div>
      </div>
    </div>
  );
}

function QuickActionCard({ icon: Icon, title, description }) {
  return (
    <button className="group backdrop-blur-xl bg-black/5 border border-black/10 rounded-2xl p-6 shadow-lg hover:bg-black/10 hover:border-black/20 hover:scale-[1.02] transition-all duration-300 text-left w-full">
      <div className="flex items-start gap-4">
        <div className="p-3 rounded-xl bg-black/10 border border-black/20 group-hover:bg-black/20 transition-all">
          <Icon size={24} className="text-black" />
        </div>
        <div>
          <h3 className="font-semibold text-black text-lg">{title}</h3>
          <p className="text-sm text-gray-600 mt-2">{description}</p>
        </div>
      </div>
    </button>
  );
}

function InfoRow({ label, value, status }) {
  return (
    <div className="flex items-center justify-between py-4 border-b border-black/10 last:border-0">
      <span className="text-gray-600 font-medium">{label}</span>
      <div className="flex items-center gap-3">
        {status === 'success' && (
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        )}
        <span className="font-semibold text-black">{value}</span>
      </div>
    </div>
  );
}