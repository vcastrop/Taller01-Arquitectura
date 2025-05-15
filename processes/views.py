

from django.shortcuts import render
from algoritmos.fcfs import fcfs
from algoritmos.RR   import rr

def index(request):
    results = gantt = avg_wt = avg_tat = None

    if request.method == 'POST':

        data = []
        count = int(request.POST.get('count', 0))
        for i in range(1, count+1):
            at = request.POST.get(f'at_{i}')
            bt = request.POST.get(f'bt_{i}')
            if at and bt:
                data.append({'no': i, 'at': int(at), 'bt': int(bt)})


        algo = request.POST['algorithm']
        if algo == 'RR':
            # Si eligió Round Robin, tomo el quantum
            tq = int(request.POST['quantum'])
        else:
            # Para FCFS u otros, no hace falta quantum
            tq = None


        if algo == 'RR':
            # guardo el burst original para cálculo de WT
            for p in data:
                p['original_bt'] = p['bt']
            proc = rr(data, tq)
        else:  # FCFS
            proc = fcfs(data)




        results = proc['table']
        gantt   = proc['gantt']

        SCALE = 20

        for seg in gantt:
            seg['left'] = seg['start'] * SCALE
            seg['width'] = (seg['stop'] - seg['start']) * SCALE

        if results and len(results) > 0:
            avg_wt = sum(p['wt'] for p in results) / len(results)
            avg_tat = sum(p['tat'] for p in results) / len(results)
        else:
            avg_wt = avg_tat = None


    return render(request, 'processes/processes.html', {
        'results': results,
        'gantt':   gantt,
        'avg_wt':  avg_wt,
        'avg_tat': avg_tat,
    })
