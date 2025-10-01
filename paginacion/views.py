from django.shortcuts import render
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import PageRequestForm
from algoritmos.factory import get_page_replacement

class PaginacionView(FormView):
    """
    FormView que valida entradas con Django Forms y ejecuta el algoritmo
    mediante la Factory. No cambia la plantilla ni la salida.
    """
    template_name = 'paginacion/paginacion.html'
    form_class = PageRequestForm
    success_url = reverse_lazy('paginacion:index')  # se usa si quisieras redirect

    def form_valid(self, form):
        data = form.to_algo_input()
        alg_name = form.cleaned_data["algorithm"]          # "fifo" / "lru" (minúsculas)
        page_alg = get_page_replacement(alg_name)
        resultado = page_alg(data)

        # normaliza clave como ya hacías en la FBV
        if resultado and "hit-ratio" in resultado:
            resultado["hit_ratio"] = resultado.pop("hit-ratio")

        context = self.get_context_data(form=form, resultado=resultado)
        return self.render_to_response(context)

    def form_invalid(self, form):
        # Renderiza la misma plantilla mostrando errores del form
        return self.render_to_response(self.get_context_data(form=form, resultado=None))


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
