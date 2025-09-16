from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import UploadImage
from .serializer import UploadedImageSerializer

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from .engine import engine

@csrf_exempt
def upload(request):
    """
    GET  -> Quick readiness check in browser.
    POST -> Accepts multipart/form-data with a file field named 'file'.
            Returns dynamic values so you can confirm it's the backend.
    """
    if request.method == "GET":
        return JsonResponse({"ok": True, "detail": "upload endpoint is ready; POST a file"})

    if request.method == "POST":
        f = request.FILES.get("file")
        
        if not f:
            return HttpResponseBadRequest("file missing")

        # Log to Django console for verification
        print(f"[upload] Received file: name={f.name}, size={f.size} bytes")

        engine.download_image_file(f)

        # Make response dynamic to prove it's the backend
        size = f.size or 1
        stock_percentage = round((size % 97) + 1.0, 2)  # 1..98 based on size
        ext = f.name.rsplit(".", 1)[-1].lower() if "." in f.name else "unknown"

        return JsonResponse({
            "stock_percentage": stock_percentage,
            "type": f"backend-{ext}",
        })

    return HttpResponseNotAllowed(["GET", "POST"])

class UploadedImageViewSet(viewsets.ModelViewSet):
    queryset = UploadImage.objects.all()
    serializer_class = UploadedImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)