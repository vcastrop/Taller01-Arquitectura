# processes/urls.py
from django.urls import path
from . import views

app_name = 'processes'

urlpatterns = [
    path('', views.index, name='index'),
    # aquí luego agregas más rutas si necesitas
]
