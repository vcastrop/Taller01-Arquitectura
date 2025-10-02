from algoritmos.factory import get_page_replacement
from algoritmos.adapters import PageResultAdapter
import io, base64

class ComparisonService:
    """
    Fachada: ejecuta N algoritmos (usando la Factory), adapta sus salidas
    y devuelve estructuras listas para mostrar (tabla y, opcional, gráfico).
    """

    def compare(self, size: int, requests: list[int], algorithms: list[str]):
        rows = []
        chart = {"labels": [], "hit_ratio": [], "faults": []}

        for key in algorithms:
            fn = get_page_replacement(key)   # 'fifo' / 'lru'
            raw = fn({"size": size, "requests": requests})
            norm = PageResultAdapter.normalize(raw)
            metrics = PageResultAdapter.to_metrics(norm)

            rows.append({
                "algorithm": key,
                "metrics": metrics,
            })

            # preparar datos para gráfico (si existen)
            chart["labels"].append(key.upper())
            chart["hit_ratio"].append(norm.get("hit_ratio"))
            chart["faults"].append(norm.get("faults"))

        return {"rows": rows, "chart": chart}

    def render_chart_base64(self, chart: dict) -> str | None:
        """
        Genera una imagen (png) de barras con hit_ratio y faults si matplotlib está disponible.
        Import 'perezoso' para no romper si no está instalada la librería.
        """
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except ModuleNotFoundError:
            return None

        labels = chart.get("labels") or []
        hit_ratio = chart.get("hit_ratio") or []
        faults = chart.get("faults") or []

        # construir la figura
        fig, ax1 = plt.subplots(figsize=(10, 5))
        x = list(range(len(labels)))

        # barras de hit_ratio (escala 0..1)
        ax1.bar(x, [hr if hr is not None else 0 for hr in hit_ratio])
        ax1.set_ylabel("hit_ratio (0..1)")
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels)

        # opcional: mostrar faults como texto arriba
        for i, f in enumerate(faults):
            if f is not None:
                ax1.text(i, (hit_ratio[i] or 0) + 0.02, f"faults={f}", ha='center', va='bottom', fontsize=9)

        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)
        return img64
