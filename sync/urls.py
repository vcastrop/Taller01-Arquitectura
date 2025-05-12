from django.urls import path
from . import views

app_name = 'sync'
urlpatterns = [
    path('', views.index, name='index'),
]