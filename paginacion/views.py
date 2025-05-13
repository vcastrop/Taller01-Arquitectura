# paginacion/views.py

from django.shortcuts import render
from algoritmos.fifo import fifo
from algoritmos.lru  import lru

def index(request):
    resultado = None

    if request.method == 'POST':
        size    = int(request.POST.get('size', 0))
        raw     = request.POST.get('requests', '')
        requests = [int(x) for x in raw.split(',') if x.strip().isdigit()]
        algo    = request.POST.get('algorithm')
        data    = {'size': size, 'requests': requests}

        if algo == 'FIFO':
            resultado = fifo(data)
        else:  # LRU
            resultado = lru(data)

        # ←── Aquí renombramos la clave 'hit-ratio' a 'hit_ratio' ──→
        if resultado and 'hit-ratio' in resultado:
            resultado['hit_ratio'] = resultado.pop('hit-ratio')

    return render(request,
                  'paginacion/paginacion.html',
                  { 'resultado': resultado })
