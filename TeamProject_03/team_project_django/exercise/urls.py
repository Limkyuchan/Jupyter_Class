from django.urls import path
from . import views

app_name = 'exercise'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('image/', views.image, name='image'),
    path('machine/', views.machine_model, name="machine"),
]

