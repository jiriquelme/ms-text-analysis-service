from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_process_image, name='test_process_image'),
]
