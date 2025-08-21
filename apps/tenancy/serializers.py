from .models import Tenant
from rest_framework import serializers


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'domain_url', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id','created_at', 'updated_at']