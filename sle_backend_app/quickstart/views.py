from django.shortcuts import render

from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from sle_backend_app.quickstart.serializer import UserSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]