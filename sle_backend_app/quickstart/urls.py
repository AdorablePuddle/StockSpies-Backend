from django.urls import re_path, path
from . import views
from .views import UserListCreateView, UserDetailView

urlpatterns = [
    # Accept both /upload and /upload/
    re_path(r'^upload/?$', views.upload, name='upload'),
    path('users/', UserListCreateView.as_view(), name = 'user_list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name = 'user_detail'),
]