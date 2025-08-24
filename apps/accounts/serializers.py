from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from apps.tenancy.models import Tenant
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("seller", "Seller"),
        )
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, default="customer")
    tenant_id = serializers.PrimaryKeyRelatedField(
        queryset=Tenant.objects.all(), source="tenant", write_only=True
    )

    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "password2", "tenant_id", "role"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.") 
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
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