from .models import Tenant
from .serializers import TenantSerializer
from rest_framework import viewsets

class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Tenant.objects.all()
        
        tenant = getattr(self.request, "tenant", None)
        if tenant:
            return Tenant.objects.filter(id=tenant.id)
        return Tenant.objects.none()
 
    
    def perform_update(self, serializer):
        tenant = getattr(self.request, "tenant", None)
        if tenant:
            serializer.save(id=tenant.id)
