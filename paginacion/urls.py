# memory/urls.py
from django.urls import path
from . import views

app_name = 'paginacion'

urlpatterns = [
    path('', views.index, name='index'),
]
