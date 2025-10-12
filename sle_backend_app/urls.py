from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sle_backend_app.quickstart.urls')),
    
    path("api/login/", TokenObtainPairView.as_view(), name = "token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name = "token_refresh"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)