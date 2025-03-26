from django.core.files.uploadedfile import UploadedFile
import pymupdf

def read_uploaded_file(file_object: UploadedFile, file_extension: str)-> str: 
    with pymupdf.open(stream=file_object.read(), filetype=file_extension) as document:
        text= ""
        for page_num in range(len(document)):
            page =  document.load_page(page_num)
            text+= page.get_text()
    return text
