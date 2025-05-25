from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import matplotlib.pyplot as plt
import io
import base64
from algoritmos.fcfs2 import fcfs2 as fcfs
from algoritmos.sstf import sstf
from algoritmos.scan import scan

@csrf_exempt
def disk_view(request):
    result = None

    if request.method == 'POST':
        current = int(request.POST['current'])
        previous = int(request.POST['previous'])
        requests = list(map(int, request.POST['requests'].strip().split()))
        cylinders = int(request.POST['cylinders'])
        algorithm = request.POST['algorithm']

        if algorithm == 'fcfs':
            order, total = fcfs(current, requests)
        elif algorithm == 'sstf':
            order, total = sstf(current, requests)
        elif algorithm == 'scan':
            order, total = scan(current, previous, requests, cylinders)
        else:
            order, total = [], 0

        # Crear gráfica tipo "línea de cilindros"
        fig, ax = plt.subplots(figsize=(12, 6))
        x = order
        y = list(range(len(order)))

        ax.set_yticks([])
        ax.set_xticks(sorted(set(x)))
        ax.set_xlabel("Número de Cilindro")
        ax.set_title(f"{algorithm.upper()} Scheduling")
        ax.invert_yaxis()

        for i in range(len(x) - 1):
            ax.annotate('', xy=(x[i + 1], i + 1), xytext=(x[i], i),
                        arrowprops=dict(arrowstyle='->', color='green'))

        ax.scatter(x, y, color='green')
        plt.grid(True, axis='x')

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()

        result = {
            'seek_time': total,
            'graph': image_base64
        }

    return render(request, 'disk/disk.html', {'result': result})
