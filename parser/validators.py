from django.core.files.uploadedfile import UploadedFile
import os
from django.forms import ValidationError


VALID_EXTENSIONS = [
    ".pdf",".doc",".docx"
]

def validate_file_extension(file_object: UploadedFile):
    ext: str  = os.path.splitext(file_object.name)[1]
    if ext.lower() not in VALID_EXTENSIONS:
        raise ValidationError(f"{ext} detected, Please Upload Valid file.")
    return ext

def validate_file_size(file_object: UploadedFile):
    MAX_UPLOAD_SIZE = 2_096_152 # in bytes
    if file_object.size > MAX_UPLOAD_SIZE:
        raise ValidationError("Max file size is 2MB")