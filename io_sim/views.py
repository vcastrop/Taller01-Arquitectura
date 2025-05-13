from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from algoritmos.io_simulador import simular_empleados_con_impresora

cola_global = []
cola_backup = []

@csrf_exempt
def index(request):
    global cola_global, cola_backup
    resultado = None

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        duracion = request.POST.get('duracion')
        prioridad = request.POST.get('prioridad')
        accion = request.POST.get('action')

        if nombre and duracion and prioridad:
            solicitud = {
                'id': nombre,
                'duracion': float(duracion),
                'prioridad': int(prioridad),
            }
            if accion == 'add':
                cola_global.append(solicitud)
            elif accion == 'simulate':
                cola_global.append(solicitud)
                cola_backup = cola_global[:]
                cola_ordenada = sorted(cola_backup, key=lambda x: x['prioridad'])
                resultado = simular_empleados_con_impresora(cola_ordenada)
                cola_global = []

    return render(request, 'io_sim/io_sim.html', {
        'queue': cola_backup if resultado else cola_global,
        'result': resultado,
    })
