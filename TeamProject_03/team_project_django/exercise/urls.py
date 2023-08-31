from django.urls import path
from . import views

app_name = 'exercise'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('predict/', views.predict, name='predict'),
    path('recommend/<int:id>', views.recommend, name="recommend"),
]

