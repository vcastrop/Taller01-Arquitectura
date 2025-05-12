from django.shortcuts import render

def index(request):
    # Lista de módulos a mostrar en el menú
    modules = [
        {'name': 'Gestión de procesos',     'url': 'processes:index'},
        {'name': 'Paginación (memoria)',    'url': 'memory:index'},
        {'name': 'Sincronización',          'url': 'sync:index'},
        {'name': 'Entrada/Salida',          'url': 'io_sim:index'},
        {'name': 'Planificación de disco',  'url': 'disk:index'},
    ]
    return render(request, 'menu/index.html', {'modules': modules})