__version__ = "1.0.0"
__author__ = "Moffitt Cancer Center"
__description__ = "Galaxy server integration for genomic data workflows"
from .models import (
    GalaxyInstance,
    GalaxyHistory,
    GalaxyDataset,
    GalaxyWorkflow,
    GalaxySyncJob,
    GalaxyAPIKey,
)
from .serializers import (
    GalaxyInstanceSerializer,
    GalaxyHistorySerializer,
    GalaxyDatasetSerializer,
    GalaxyWorkflowSerializer,
    GalaxySyncJobSerializer,
    GalaxyAPIKeySerializer,
    GalaxyInstanceCreateSerializer,
    GalaxyDatasetProcessSerializer,
    GalaxySyncJobCreateSerializer,
    GalaxyStatisticsSerializer,
)
from .views import (
    GalaxyInstanceViewSet,
    GalaxyHistoryViewSet,
    GalaxyDatasetViewSet,
    GalaxyWorkflowViewSet,
    GalaxySyncJobViewSet,
    GalaxyAPIKeyViewSet,
    StandardResultsSetPagination,
)
from .filters import (
    GalaxyInstanceFilter,
    GalaxyDatasetFilter,
    GalaxyWorkflowFilter,
)
from .apps import GalaxyIntegrationConfig
from .urls import urlpatterns
__all__ = [
    '__version__',
    '__author__',
    '__description__',
    'GalaxyInstance',
    'GalaxyHistory',
    'GalaxyDataset',
    'GalaxyWorkflow',
    'GalaxySyncJob',
    'GalaxyAPIKey',
    'GalaxyInstanceSerializer',
    'GalaxyHistorySerializer',
    'GalaxyDatasetSerializer',
    'GalaxyWorkflowSerializer',
    'GalaxySyncJobSerializer',
    'GalaxyAPIKeySerializer',
    'GalaxyInstanceCreateSerializer',
    'GalaxyDatasetProcessSerializer',
    'GalaxySyncJobCreateSerializer',
    'GalaxyStatisticsSerializer',
    'GalaxyInstanceViewSet',
    'GalaxyHistoryViewSet',
    'GalaxyDatasetViewSet',
    'GalaxyWorkflowViewSet',
    'GalaxySyncJobViewSet',
    'GalaxyAPIKeyViewSet',
    'StandardResultsSetPagination',
    'GalaxyInstanceFilter',
    'GalaxyDatasetFilter',
    'GalaxyWorkflowFilter',
    'GalaxyIntegrationConfig',
    'urlpatterns',
]

def get_active_galaxy_instances():
    return GalaxyInstance.objects.filter(is_active=True)

def get_vcf_datasets():
    return GalaxyDataset.objects.filter(is_vcf=True)

def get_unprocessed_vcf_datasets():
    return GalaxyDataset.objects.filter(is_vcf=True, is_processed=False)

def get_running_workflows():
    return GalaxyWorkflow.objects.filter(status='running')

def get_active_sync_jobs():
    return GalaxySyncJob.objects.filter(status__in=['pending', 'running'])
__all__.extend([
    'get_active_galaxy_instances',
    'get_vcf_datasets',
    'get_unprocessed_vcf_datasets',
    'get_running_workflows',
    'get_active_sync_jobs',
])
