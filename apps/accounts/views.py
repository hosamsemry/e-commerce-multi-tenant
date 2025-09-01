from rest_framework import generics
from .serializers import  UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from .permissions import IsSameTenant

User = get_user_model()


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser, IsSameTenant]

    def get_queryset(self):
        return User.objects.filter(tenant_id=self.request.user.tenant_id)
