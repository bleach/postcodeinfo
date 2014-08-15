from .models import Address

from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    point = serializers.Field(source='point_geojson')

    class Meta:
        model = Address
        fields = ('uprn', 'building_name', 'sub_building_name',
                  'building_number', 'thoroughfare_name',
                  'dependent_locality', 'post_town', 'postcode', 'point')
