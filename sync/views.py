from django.shortcuts import render
from algoritmos.dining import simulate_dining
from algoritmos.producer_consumer import simulate_pc

def dining_philosophers(request):
    # valores por defecto
    n = 5
    iterations = 1
    logs = None

    if request.method == 'POST':
        n = int(request.POST.get('n', n))
        iterations = int(request.POST.get('iterations', iterations))
        logs = simulate_dining(n, iterations)

    return render(request, 'sync/dining.html', {
        'n': n,
        'iterations': iterations,
        'logs': logs,
    })

def producer_consumer(request):
    # valores por defecto
    size       = 20
    prod_prio  = 6.0
    cons_prio  = 2.0
    variation  = 2.0
    logs       = None

    if request.method == 'POST':
        size      = int(request.POST.get('size', size))
        prod_prio = float(request.POST.get('prod_prio', prod_prio))
        cons_prio = float(request.POST.get('cons_prio', cons_prio))
        variation = float(request.POST.get('variation', variation))

        # ejecutamos la simulación y recogemos el log
        logs = simulate_pc(size, prod_prio, cons_prio, variation)

    return render(request, 'sync/prodcon.html', {
        'size': size,
        'prod_prio': prod_prio,
        'cons_prio': cons_prio,
        'variation': variation,
        'logs': logs,
    })


def index(request):
    """
    Menú de sincronización: enlaces a prodcon y dining.
    """
    return render(request, 'sync/index.html')
