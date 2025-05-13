from django.urls import path
from . import views
urlpatterns = [
    path('', views.disk_view, name='index'),
]