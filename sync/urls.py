from django.urls import path
from . import views

app_name = 'sync'

urlpatterns = [
    # Menú principal de sincronización
    path('',          views.dining_philosophers,                 name='index'),
    path('prodcon/', views.producer_consumer, name='prodcon'),
]
