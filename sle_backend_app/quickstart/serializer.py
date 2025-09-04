from rest_framework import serializers
from .models import UploadImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ["id", "image", "uploaded_at"]