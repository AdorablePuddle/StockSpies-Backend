from django.db import models

# Create your models here.
class UploadImage(models.Model):
    image = models.ImageField(upload_to = "upload")
    uploaded_at = models.DateTimeField(auto_now_add = True)