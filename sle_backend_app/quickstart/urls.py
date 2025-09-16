from django.urls import re_path
from . import views

urlpatterns = [
    # Accept both /upload and /upload/
    re_path(r'^upload/?$', views.upload, name='upload'),
]