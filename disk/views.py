from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from algoritmos.factory import get_disk_scheduler
import io, base64  # estos sí pueden ir arriba

def _render_plot(order, alg_name):
    # Import perezoso: solo se ejecuta cuando realmente generas la imagen
    import matplotlib
    matplotlib.use('Agg')  # backend no interactivo para servidores
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12, 6))
    x = order
    y = list(range(len(order)))

    ax.set_yticks([])
    ax.set_xticks(sorted(set(x)))
    ax.set_xlabel("Número de Cilindro")
    ax.set_title(f"{alg_name.upper()} Scheduling")
    ax.invert_yaxis()

    for i in range(len(x) - 1):
        ax.annotate('', xy=(x[i + 1], i + 1), xytext=(x[i], i),
                    arrowprops=dict(arrowstyle='->'))

    ax.scatter(x, y)
    plt.grid(True, axis='x')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    plt.close(fig)
    return image_base64


@csrf_exempt  # cuando tengas {% csrf_token %} en el form, quítalo
def disk_view(request):
    result = None

    if request.method == 'POST':
        # --- leer entradas ---
        current   = int(request.POST['current'])
        previous  = int(request.POST['previous'])
        cylinders = int(request.POST['cylinders'])
        raw       = (request.POST.get('requests') or '').strip()
        parts     = raw.replace(',', ' ').split()
        requests  = [int(x) for x in parts if x.isdigit()]
        alg_name  = request.POST.get('algorithm', 'sstf')  # "fcfs"/"sstf"/"scan"

        # --- seleccionar y ejecutar algoritmo (Factory) ---
        disk_alg = get_disk_scheduler(alg_name)
        order, total = disk_alg(current, previous, requests, cylinders)

        # --- generar gráfica (si matplotlib está disponible) ---
        try:
            image_base64 = _render_plot(order, alg_name)
        except ModuleNotFoundError:
            # Si no está instalado matplotlib, no rompemos la vista
            image_base64 = None

        result = {
            'seek_time': total,
            'graph': image_base64
        }

    return render(request, 'disk/disk.html', {'result': result})
