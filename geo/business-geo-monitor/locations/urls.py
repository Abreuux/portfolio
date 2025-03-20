from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusinessLocationViewSet, MapView

router = DefaultRouter()
router.register(r'businesses', BusinessLocationViewSet, basename='business')

urlpatterns = [
    path('', MapView.as_view(), name='map'),
    path('api/', include(router.urls)),
] 