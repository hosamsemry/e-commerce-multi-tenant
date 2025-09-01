from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from apps.tenancy.models import Tenant
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name","last_name", "email","password"]

    def create(self, validated_data):
        request = self.context.get('request')
        tenant = getattr(request, 'tenant', None) if request else None
        if not tenant:
            raise serializers.ValidationError('Tenant could not be determined from request context.')
        
        password = validated_data.pop("password")  
        user = User(**validated_data)
        user.tenant = tenant
        user.is_active = False
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["tenant_id"] = str(user.tenant_id)
        token["role"] = user.role

        return token

class UserSerializer(serializers.ModelSerializer):
    tenant = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ["id", "email", "username", "role", "tenant"]