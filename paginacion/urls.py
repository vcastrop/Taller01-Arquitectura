from django.urls import path
from .views import index, PaginacionView
from .views_compare import CompareView

app_name = "paginacion"

urlpatterns = [
    path('', PaginacionView.as_view(), name='index'),
    path('fbv/', index, name='index_fbv'),
    path('compare/', CompareView.as_view(), name='compare'),
]
