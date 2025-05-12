from django.urls import path
from . import views

app_name = 'io_sim'
urlpatterns = [
    path('', views.index, name='index'),
]