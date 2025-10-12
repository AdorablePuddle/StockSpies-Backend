from rest_framework import permissions, viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import UploadImage
from .serializer import UploadedImageSerializer, UserSerializer

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .engine import engine

@api_view(["GET", "POST"])
@permission_classes(IsAuthenticated)
def upload(request):
    if request.method == "GET":
        return JsonResponse({"ok": True, "detail": "upload endpoint is ready; POST a file"})

    if request.method == "POST":
        f = request.FILES.get("file")

        if not f:
            return HttpResponseBadRequest("file missing")

        # Log to Django console for verification
        print(f"[upload] Received file: name={f.name}, size={f.size} bytes")

        # Make response dynamic to prove it's the backend
        size = f.size or 1
        # stock_percentage = round((size % 97) + 1.0, 2)  # 1..98 based on size
        produce, stock_level = "", 0
        try:
            produce, stock_level = engine.get_prediction(f)
        except RuntimeError as E:
            return HttpResponseBadRequest(E.args)
        except ValueError as E:
            return HttpResponseBadRequest(E.args)
        ext = f.name.rsplit(".", 1)[-1].lower() if "." in f.name else "unknown"

        return JsonResponse({            
            "stock_percentage": float(stock_level) * 100,
            "type": produce,
        })

    return HttpResponseNotAllowed(["GET", "POST"])

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadImage.objects.all()
    serializer_class = UploadedImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
