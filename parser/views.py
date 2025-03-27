from django.forms import ValidationError
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .utils import read_uploaded_file, extract_info
from .validators import validate_file_extension, validate_file_size
from django.core.files.uploadedfile import UploadedFile


# Create your views here.
def home(request: HttpRequest):
    return render(request, "index.html")

def upload_resume(request: HttpRequest):
    if request.method == "POST" and request.FILES.get("file"):
        file: UploadedFile = request.FILES["file"]
        try:
            ext: str = validate_file_extension(file)
            validate_file_size(file)
            file_content= read_uploaded_file(file, ext)
            data = extract_info(file_content)
            print("file content>>", file_content)
        except ValidationError as err:
            return JsonResponse({"error": err.message})
            
    return JsonResponse({"error": "invalid request"}, status=400)

