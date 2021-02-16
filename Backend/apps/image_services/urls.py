from django.urls import path
from apps.image_services.views import ProcessImage

urlpatterns = [
    path('image/process', ProcessImage.as_view(), name='image-process'),
]
