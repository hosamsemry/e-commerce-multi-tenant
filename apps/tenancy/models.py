from django.db import models

class Tenant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    domain_url = models.URLField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
