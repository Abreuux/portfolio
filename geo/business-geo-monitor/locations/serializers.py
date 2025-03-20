from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import BusinessLocation

class BusinessLocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = BusinessLocation
        geo_field = "location"
        fields = (
            'id', 'name', 'description', 'address', 'city', 'state',
            'postal_code', 'phone', 'email', 'website', 'location',
            'radius', 'coverage_area', 'business_type', 'opening_hours',
            'is_active', 'customer_count', 'revenue', 'created_at',
            'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')
    
    def validate_location(self, value):
        """Valida se a localização está dentro dos limites do Brasil"""
        if not (-73.9872 <= value.x <= -34.7929 and -33.7683 <= value.y <= 5.2723):
            raise serializers.ValidationError(
                "A localização deve estar dentro dos limites do Brasil"
            )
        return value
    
    def validate_radius(self, value):
        """Valida se o raio é apropriado para o tipo de negócio"""
        business_type = self.initial_data.get('business_type', '')
        if business_type.lower() in ['restaurante', 'café', 'loja'] and value > 5:
            raise serializers.ValidationError(
                f"O raio de atuação para {business_type} não deve exceder 5km"
            )
        return value 