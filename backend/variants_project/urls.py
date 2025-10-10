"""
URL configuration for variants_project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from variants import views as variant_views

# API Router
router = routers.DefaultRouter()
router.register(r'variants', variant_views.VariantViewSet)
router.register(r'clinical-significance', variant_views.ClinicalSignificanceViewSet)
router.register(r'annotations', variant_views.AnnotationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/galaxy/', include('galaxy_integration.urls')),
    path('api/annotations/', include('annotations.urls')),
]

