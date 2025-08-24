from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user.tenant)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ListUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
