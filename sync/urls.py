from django.urls import path
from . import views

app_name = 'sync'

urlpatterns = [


    path('', views.index, name='index'),
    path('dining/',          views.dining_philosophers,                 name='dining'),
    path('prodcon/', views.producer_consumer, name='prodcon'),
]
