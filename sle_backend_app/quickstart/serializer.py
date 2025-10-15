from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UploadImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ["id", "image", "uploaded_at"]

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {
            "password" : {"write_only": True},
        }
    
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)