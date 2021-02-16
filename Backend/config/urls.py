
# from django.urls import path, re_path #,  include
from django.conf.urls import include, url

urlpatterns = [
    url('api/', include(('apps.image_services.urls', 'image'), namespace='image')),
]
