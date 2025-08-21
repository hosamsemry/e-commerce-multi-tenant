from django.utils.deprecation import MiddlewareMixin
from .models import Tenant
from django.db import connection

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split(":")[0]
        try:
            tenant = Tenant.objects.get(domain_url=host, is_active=True)
            request.tenant = tenant

            with connection.cursor() as cursor:
                cursor.execute("SET app.current_tenant = %s", [str(tenant.id)])

        except Tenant.DoesNotExist:
            request.tenant = None
