from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sources', views.AnnotationSourceViewSet)
router.register(r'jobs', views.AnnotationJobViewSet)
router.register(r'variant-annotations', views.VariantAnnotationViewSet)
router.register(r'clinvar', views.ClinVarAnnotationViewSet)
router.register(r'cosmic', views.COSMICAnnotationViewSet)
router.register(r'civic', views.CIViCAnnotationViewSet)
router.register(r'cache', views.AnnotationCacheViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
