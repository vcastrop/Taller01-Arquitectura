# memory/views.py
from django.shortcuts import render

def index(request):
    """
    Renderiza la página principal del módulo de paginación de memoria.
    Más adelante aquí recibiremos formularios y mostraremos resultados.
    """
    return render(request, 'paginacion/paginacion.html')
