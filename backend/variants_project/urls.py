"""
URL configuration for variants_project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from variants import views as variant_views
from variants import aws_views
from variants import gemini_views
from variants import ai_views
from variants.debug_views import debug_statistics
from variants.aws_views import aws_health_check

router = routers.DefaultRouter()
router.register(r'variants', variant_views.VariantViewSet)
router.register(r'variants-llm', gemini_views.VariantLLMViewSet, basename='variant-llm')
router.register(r'clinical-significance', variant_views.ClinicalSignificanceViewSet)
router.register(r'annotations', variant_views.AnnotationViewSet)
router.register(r'aws/files', aws_views.AWSFileUploadViewSet, basename='aws-files')
router.register(r'aws/annotation-jobs', aws_views.AWSAnnotationJobViewSet, basename='aws-annotation-jobs')
router.register(r'aws/sync-jobs', aws_views.AWSSyncJobViewSet, basename='aws-sync-jobs')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/variants/natural_language_search/', gemini_views.NaturalLanguageSearchView.as_view()),
    path('api/variants/chat/', gemini_views.VariantChatView.as_view()),
    path('api/variants/debug-statistics/', debug_statistics, name='debug-statistics'),
    path('api/ai/trend-prediction/', ai_views.TrendPredictionView.as_view(), name='trend-prediction'),
    path('api/ai/generate-graph/', ai_views.GraphGenerationView.as_view(), name='generate-graph'),
    path('api/ai/variant-statistics-graph/', ai_views.VariantStatisticsGraphView.as_view(), name='variant-statistics-graph'),
    path('api/galaxy/', include('galaxy_integration.urls')),
    path('api/annotations/', include('annotations.urls')),
    path('api/aws/health/', aws_health_check, name='aws-health-check'),
]

