from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name="home_page"),
    path('upload_resume', views.upload_resume, name="upload_resume"),
]
