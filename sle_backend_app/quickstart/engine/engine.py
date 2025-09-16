from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage

def download_image_file(f : InMemoryUploadedFile):
    print(f"[upload] Download image")
    FileSystemStorage(location = "./tmpfiles/").save(f.name, f)