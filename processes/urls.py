from django.urls import path
from .views import index, ProcessesView

app_name = "processes"

urlpatterns = [
    path('', ProcessesView.as_view(), name='index'),  # CBV (patrón Django)
    path('fbv/', index, name='index_fbv'),            # FBV original (respaldo)
]