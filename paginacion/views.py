from django.shortcuts import render
from algoritmos.factory import get_page_replacement  # ← NUEVO


def index(request):
    resultado = None

    if request.method == 'POST':
        # --- leer y preparar entradas ---
        try:
            size = int(request.POST.get('size', 0))
        except (TypeError, ValueError):
            size = 0

        raw = request.POST.get('requests', '')
        requests = [int(x) for x in raw.split(',') if x.strip().isdigit()]

        algo = request.POST.get('algorithm', 'FIFO')  # "FIFO" o "LRU"
        data = {'size': size, 'requests': requests}

        # --- seleccionar algoritmo mediante la Factory ---
        page_alg = get_page_replacement(algo)  # la factory normaliza el nombre
        resultado = page_alg(data)

        # --- normalizar clave para la plantilla (opcional) ---
        if resultado and 'hit-ratio' in resultado:
            resultado['hit_ratio'] = resultado.pop('hit-ratio')

    return render(
        request,
        'paginacion/paginacion.html',
        {'resultado': resultado}
    )
