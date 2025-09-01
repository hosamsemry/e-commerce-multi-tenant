from .models import Tenant
from .serializers import TenantSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSerializer
    permission_classes = [IsAdminUser]
    queryset = Tenant.objects.all() 
    
    def perform_update(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        if tenant:
            serializer.save(id=tenant.id)
