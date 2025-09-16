from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import FileSystemStorage

tmpfiles = "./tmpfiles/"

def download_image_file(f : InMemoryUploadedFile):
    print(f"[upload] Download image")
    FileSystemStorage(location = tmpfiles).save(f.name, f)

def get_prediction(f : InMemoryUploadedFile):
    download_image_file(f)
    file_name = f.name
        