import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import LoadingSpinner from '../components/LoadingSpinner';
import  api  from '../services/api';
import { Dna, Network, FileText, TrendingUp, AlertCircle } from 'lucide-react';

export default function Dashboard() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const response = await api.get('/variants/');
      const variants = response.data.results || [];
      
      // Calculate statistics
      const impactCounts = {
        HIGH: 0,
        MODERATE: 0,
        LOW: 0,
        MODIFIER: 0,
      };

      const geneCounts = {};
      let pathogenicCount = 0;

      variants.forEach(v => {
        if (v.impact) impactCounts[v.impact]++;
        if (v.gene_symbol) {
          geneCounts[v.gene_symbol] = (geneCounts[v.gene_symbol] || 0) + 1;
        }
        if (v.clinical_significance?.some(cs => cs.is_pathogenic)) {
          pathogenicCount++;
        }
      });

      return {
        totalVariants: variants.length,
        pathogenicVariants: pathogenicCount,
        impactCounts,
        topGenes: Object.entries(geneCounts)
          .sort((a, b) => b[1] - a[1])
          .slice(0, 5)
          .map(([gene, count]) => ({ name: gene, count })),
      };
    },
  });

  if (isLoading) return <LoadingSpinner />;

  const impactData = stats ? [
    { name: 'HIGH', value: stats.impactCounts.HIGH },
    { name: 'MODERATE', value: stats.impactCounts.MODERATE },
    { name: 'LOW', value: stats.impactCounts.LOW },
    { name: 'MODIFIER', value: stats.impactCounts.MODIFIER },
  ] : [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Welcome to Moffitt Variants Analysis</p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          icon={Dna}
          label="Total Variants"
          value={stats?.totalVariants || 0}
          color="blue"
        />
        <MetricCard
          icon={AlertCircle}
          label="Pathogenic"
          value={stats?.pathogenicVariants || 0}
          color="red"
        />
        <MetricCard
          icon={TrendingUp}
          label="High Impact"
          value={stats?.impactCounts.HIGH || 0}
          color="orange"
        />
        <MetricCard
          icon={Network}
          label="Unique Genes"
          value={stats?.topGenes?.length || 0}
          color="purple"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Impact Distribution */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Variant Impact Distribution
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={impactData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Top Genes */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Top Genes by Variant Count
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart
              data={stats?.topGenes || []}
              layout="vertical"
              margin={{ left: 100 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis dataKey="name" type="category" width={100} />
              <Tooltip />
              <Bar dataKey="count" fill="#8b5cf6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <QuickActionCard
          icon={Dna}
          title="Browse Variants"
          description="View and filter all genetic variants"
          link="/variants"
          color="blue"
        />
        <QuickActionCard
          icon={Network}
          title="Variant Network"
          description="Explore gene-variant relationships"
          link="/network"
          color="purple"
        />
        <QuickActionCard
          icon={FileText}
          title="Annotations"
          description="View detailed variant annotations"
          link="/annotations"
          color="green"
        />
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          System Information
        </h2>
        <div className="space-y-3">
          <InfoRow label="Database" value="SQLite (Development)" />
          <InfoRow label="API Status" value="Active" status="success" />
          <InfoRow label="Last Updated" value="Just now" />
        </div>
      </div>
    </div>
  );
}

function MetricCard({ icon: Icon, label, value, color }) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    red: 'bg-red-50 text-red-600',
    orange: 'bg-orange-50 text-orange-600',
    purple: 'bg-purple-50 text-purple-600',
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-600 text-sm font-medium">{label}</p>
          <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon size={24} />
        </div>
      </div>
    </div>
  );
}

function QuickActionCard({ icon: Icon, title, description, link, color }) {
  const colorClasses = {
    blue: 'hover:border-blue-300 hover:bg-blue-50',
    purple: 'hover:border-purple-300 hover:bg-purple-50',
    green: 'hover:border-green-300 hover:bg-green-50',
  };

  return (
    <Link
      to={link}
      className={`bg-white rounded-lg shadow-md p-6 border-2 border-transparent transition-all ${colorClasses[color]}`}
    >
      <div className="flex items-start gap-4">
        <div className={`p-3 rounded-lg ${color === 'blue' ? 'bg-blue-100 text-blue-600' : color === 'purple' ? 'bg-purple-100 text-purple-600' : 'bg-green-100 text-green-600'}`}>
          <Icon size={24} />
        </div>
        <div>
          <h3 className="font-semibold text-gray-900">{title}</h3>
          <p className="text-sm text-gray-600 mt-1">{description}</p>
        </div>
      </div>
    </Link>
  );
}

function InfoRow({ label, value, status }) {
  return (
    <div className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
      <span className="text-gray-600">{label}</span>
      <div className="flex items-center gap-2">
        {status === 'success' && (
          <div className="w-2 h-2 bg-green-500 rounded-full"></div>
        )}
        <span className="font-medium text-gray-900">{value}</span>
      </div>
    </div>
  );
}
