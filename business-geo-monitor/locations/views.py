from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import TemplateView
from .models import BusinessLocation
from .serializers import BusinessLocationSerializer
from django.db import models

class MapView(TemplateView):
    template_name = 'map.html'

class BusinessLocationViewSet(viewsets.ModelViewSet):
    queryset = BusinessLocation.objects.all()
    serializer_class = BusinessLocationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'state', 'business_type', 'is_active']
    search_fields = ['name', 'address', 'description']
    ordering_fields = ['name', 'city', 'revenue', 'customer_count']
    ordering = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por proximidade
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        radius = self.request.query_params.get('radius', 10)  # km
        
        if lat and lng:
            point = Point(float(lng), float(lat), srid=4326)
            queryset = queryset.filter(
                location__distance_lte=(point, D(km=radius))
            ).annotate(
                distance=Distance('location', point)
            ).order_by('distance')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """Retorna negócios próximos a um ponto específico"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = request.query_params.get('radius', 10)
        
        if not lat or not lng:
            return Response(
                {'error': 'Parâmetros lat e lng são obrigatórios'},
                status=400
            )
        
        try:
            point = Point(float(lng), float(lat), srid=4326)
            queryset = self.get_queryset().filter(
                location__distance_lte=(point, D(km=radius))
            ).annotate(
                distance=Distance('location', point)
            ).order_by('distance')
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except ValueError:
            return Response(
                {'error': 'Coordenadas inválidas'},
                status=400
            )
    
    @action(detail=False, methods=['get'])
    def coverage_analysis(self, request):
        """Analisa a cobertura de negócios por região"""
        city = request.query_params.get('city')
        state = request.query_params.get('state')
        
        queryset = self.get_queryset()
        if city:
            queryset = queryset.filter(city=city)
        if state:
            queryset = queryset.filter(state=state)
        
        # Agrupa por tipo de negócio
        business_types = queryset.values('business_type').annotate(
            count=models.Count('id'),
            total_revenue=models.Sum('revenue'),
            avg_customers=models.Avg('customer_count')
        )
        
        # Calcula área total coberta
        total_coverage = queryset.aggregate(
            total_area=models.Sum('radius')
        )['total_area'] or 0
        
        return Response({
            'business_types': business_types,
            'total_coverage_km2': total_coverage,
            'total_businesses': queryset.count()
        }) 