import React, { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import LoadingSpinner from "../components/LoadingSpinner";
import api from "../services/api";
import { Play, AlertCircle, CheckCircle, Clock } from "lucide-react";

export default function GalaxyIntegration() {
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);

  const {
    data: workflowsData,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["galaxy-workflows"],
    queryFn: async () => {
      const response = await api.get("/galaxy/workflows/");
      return response.data;
    },
  });

  const runWorkflowMutation = useMutation({
    mutationFn: async (workflowId) => {
      const response = await api.post(
        `/galaxy/workflows/${workflowId}/run/`,
        {}
      );
      return response.data;
    },
  });

  if (isLoading) return <LoadingSpinner />;

  const workflows = workflowsData?.results || [];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Galaxy Integration</h1>
        <p className="text-gray-600 mt-1">
          Run bioinformatics workflows on your variant data
        </p>
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start gap-3">
          <AlertCircle
            className="text-red-600 flex-shrink-0 mt-0.5"
            size={20}
          />
          <div>
            <h3 className="font-medium text-red-900">
              Error loading workflows
            </h3>
            <p className="text-red-700 text-sm mt-1">{error.message}</p>
          </div>
        </div>
      )}

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start gap-3">
        <AlertCircle className="text-blue-600 flex-shrink-0 mt-0.5" size={20} />
        <div>
          <h3 className="font-medium text-blue-900">Galaxy Connection</h3>
          <p className="text-blue-700 text-sm mt-1">
            Connect to Galaxy to run advanced bioinformatics workflows on your
            variant data.
          </p>
        </div>
      </div>

      {/* Workflows Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {workflows.length > 0 ? (
          workflows.map((workflow) => (
            <WorkflowCard
              key={workflow.id}
              workflow={workflow}
              isSelected={selectedWorkflow?.id === workflow.id}
              onSelect={() => setSelectedWorkflow(workflow)}
              onRun={() => runWorkflowMutation.mutate(workflow.id)}
              isRunning={runWorkflowMutation.isPending}
            />
          ))
        ) : (
          <div className="col-span-full bg-white rounded-lg shadow-md p-12 text-center">
            <AlertCircle className="mx-auto text-gray-400 mb-4" size={48} />
            <p className="text-gray-500 text-lg">No workflows available</p>
            <p className="text-gray-400 text-sm mt-2">
              Configure Galaxy integration to see available workflows
            </p>
          </div>
        )}
      </div>

      {/* Selected Workflow Details */}
      {selectedWorkflow && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Workflow Details
          </h2>
          <WorkflowDetails workflow={selectedWorkflow} />
        </div>
      )}

      {/* Recent Runs */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Recent Runs
        </h2>
        <div className="space-y-3">
          <RunItem
            name="Variant Annotation Pipeline"
            status="completed"
            timestamp="2 hours ago"
          />
          <RunItem
            name="Quality Control Analysis"
            status="running"
            timestamp="30 minutes ago"
          />
          <RunItem
            name="Population Frequency Analysis"
            status="completed"
            timestamp="1 day ago"
          />
        </div>
      </div>
    </div>
  );
}

function WorkflowCard({ workflow, isSelected, onSelect, onRun, isRunning }) {
  return (
    <div
      onClick={onSelect}
      className={`bg-white rounded-lg shadow-md p-6 cursor-pointer transition-all border-2 ${
        isSelected
          ? "border-primary-500 bg-primary-50"
          : "border-transparent hover:shadow-lg"
      }`}
    >
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">
            {workflow.name}
          </h3>
          <p className="text-sm text-gray-600 mt-1">{workflow.description}</p>
        </div>
      </div>

      <div className="mb-4 space-y-2">
        <InfoItem label="Version" value={workflow.version || "-"} />
        <InfoItem label="Status" value={workflow.status || "Available"} />
      </div>

      <button
        onClick={(e) => {
          e.stopPropagation();
          onRun();
        }}
        disabled={isRunning}
        className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <Play size={18} />
        {isRunning ? "Running..." : "Run Workflow"}
      </button>
    </div>
  );
}

function WorkflowDetails({ workflow }) {
  return (
    <div className="space-y-6">
      {/* Basic Information */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-3">Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <DetailRow label="Name" value={workflow.name} />
          <DetailRow label="Version" value={workflow.version || "-"} />
          <DetailRow label="Status" value={workflow.status || "Available"} />
          <DetailRow label="Type" value={workflow.type || "-"} />
        </div>
      </div>

      {/* Description */}
      <div>
        <h3 className="font-semibold text-gray-900 mb-3">Description</h3>
        <p className="text-gray-600 bg-gray-50 rounded-lg p-4">
          {workflow.description || "No description available"}
        </p>
      </div>

      {/* Parameters */}
      {workflow.parameters && (
        <div>
          <h3 className="font-semibold text-gray-900 mb-3">Parameters</h3>
          <div className="bg-gray-50 rounded-lg p-4">
            <pre className="text-sm text-gray-600 overflow-auto">
              {JSON.stringify(workflow.parameters, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}

function DetailRow({ label, value }) {
  return (
    <div className="bg-gray-50 rounded-lg p-3">
      <p className="text-xs font-medium text-gray-600 uppercase tracking-wide">
        {label}
      </p>
      <p className="text-sm font-medium text-gray-900 mt-1">{value}</p>
    </div>
  );
}

function InfoItem({ label, value }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-sm text-gray-600">{label}</span>
      <span className="text-sm font-medium text-gray-900">{value}</span>
    </div>
  );
}

function RunItem({ name, status, timestamp }) {
  const statusConfig = {
    completed: {
      icon: CheckCircle,
      color: "text-green-600",
      bg: "bg-green-50",
    },
    running: { icon: Clock, color: "text-blue-600", bg: "bg-blue-50" },
    failed: { icon: AlertCircle, color: "text-red-600", bg: "bg-red-50" },
  };

  const config = statusConfig[status] || statusConfig.completed;
  const Icon = config.icon;

  return (
    <div
      className={`${config.bg} rounded-lg p-4 flex items-center justify-between`}
    >
      <div className="flex items-center gap-3">
        <Icon className={config.color} size={20} />
        <div>
          <p className="font-medium text-gray-900">{name}</p>
          <p className="text-sm text-gray-600">{timestamp}</p>
        </div>
      </div>
      <span className={`text-xs font-semibold uppercase ${config.color}`}>
        {status}
      </span>
    </div>
  );
}
