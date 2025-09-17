from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'instances', views.GalaxyInstanceViewSet)
router.register(r'histories', views.GalaxyHistoryViewSet)
router.register(r'datasets', views.GalaxyDatasetViewSet)
router.register(r'workflows', views.GalaxyWorkflowViewSet)
router.register(r'sync-jobs', views.GalaxySyncJobViewSet)
router.register(r'api-keys', views.GalaxyAPIKeyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
