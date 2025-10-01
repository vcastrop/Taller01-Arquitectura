from django.shortcuts import render
from algoritmos.factory import get_cpu_scheduler  # ← NUEVO: centraliza la selección de algoritmo


def index(request):
    results = gantt = avg_wt = avg_tat = None

    if request.method == 'POST':
        # --- armar los procesos desde el formulario ---
        data = []
        try:
            count = int(request.POST.get('count', 0))
        except (TypeError, ValueError):
            count = 0

        for i in range(1, count + 1):
            at = request.POST.get(f'at_{i}')
            bt = request.POST.get(f'bt_{i}')
            if at not in (None, '') and bt not in (None, ''):
                try:
                    data.append({'no': i, 'at': int(at), 'bt': int(bt)})
                except ValueError:
                    # si un campo no es numérico, lo ignoramos; puedes mostrar un error en plantilla si prefieres
                    pass

        # --- elegir algoritmo mediante la Factory ---
        alg_name = request.POST.get('algorithm', 'FCFS')  # soporta "FCFS"/"RR" (cualquier mayúsc/minúsc)
        scheduler = get_cpu_scheduler(alg_name)

        # --- parámetros específicos (solo RR necesita quantum) ---
        tq = None
        if alg_name.upper() == 'RR':
            quantum_str = request.POST.get('quantum', '')
            if quantum_str != '':
                tq = int(quantum_str)
            # conservar burst original (tu lógica actual)
            for p in data:
                p['original_bt'] = p['bt']

        # --- ejecutar el algoritmo seleccionado ---
        if tq is None:
            proc = scheduler(data)          # FCFS (u otro que no requiera quantum)
        else:
            proc = scheduler(data, tq)      # RR

        # --- preparar datos para la vista ---
        results = proc.get('table')
        gantt   = proc.get('gantt')

        SCALE = 20
        if gantt:
            for seg in gantt:
                seg['left'] = seg['start'] * SCALE
                seg['width'] = (seg['stop'] - seg['start']) * SCALE

        if results:
            avg_wt  = sum(p['wt']  for p in results) / len(results)
            avg_tat = sum(p['tat'] for p in results) / len(results)

    return render(request, 'processes/processes.html', {
        'results': results,
        'gantt':   gantt,
        'avg_wt':  avg_wt,
        'avg_tat': avg_tat,
    })


# --- Patron de diseño 1 django ---

from django.views.generic import TemplateView
from common.mixins import PostParamsMixin  # crea este mixin en el paso 2
from algoritmos.factory import get_cpu_scheduler

class ProcessesView(PostParamsMixin, TemplateView):
    """CBV que mantiene exactamente el mismo comportamiento/plantilla."""
    template_name = 'processes/processes.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            'results': None, 'gantt': None, 'avg_wt': None, 'avg_tat': None
        })

    def post(self, request, *args, **kwargs):
        results = gantt = avg_wt = avg_tat = None

        # parseo similar al de tu FBV, con pequeña ayuda del mixin
        count = self.get_int(request, 'count', 0)
        data = []
        for i in range(1, (count or 0) + 1):
            at = request.POST.get(f'at_{i}')
            bt = request.POST.get(f'bt_{i}')
            if at not in (None, '') and bt not in (None, ''):
                try:
                    data.append({'no': i, 'at': int(at), 'bt': int(bt)})
                except ValueError:
                    pass

        alg_name = request.POST.get('algorithm', 'FCFS')
        scheduler = get_cpu_scheduler(alg_name)

        tq = None
        if alg_name.upper() == 'RR':
            q = request.POST.get('quantum', '')
            if q != '':
                tq = int(q)
            for p in data:
                p['original_bt'] = p['bt']

        proc = scheduler(data) if tq is None else scheduler(data, tq)

        results = proc.get('table')
        gantt   = proc.get('gantt')

        SCALE = 20
        if gantt:
            for seg in gantt:
                seg['left']  = seg['start'] * SCALE
                seg['width'] = (seg['stop'] - seg['start']) * SCALE

        if results:
            n = len(results)
            avg_wt  = sum(p['wt']  for p in results) / n
            avg_tat = sum(p['tat'] for p in results) / n

        return self.render_to_response({
            'results': results, 'gantt': gantt,
            'avg_wt':  avg_wt,  'avg_tat': avg_tat
        })
