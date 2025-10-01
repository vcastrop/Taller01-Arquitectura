from django import forms

ALGO_CHOICES = (
    ("FIFO", "FIFO"),
    ("LRU", "LRU"),
)

class PageRequestForm(forms.Form):
    size = forms.IntegerField(min_value=1, label="Tamaño de marcos")
    requests = forms.CharField(label="Secuencia de solicitudes (coma o espacio)")

    algorithm = forms.ChoiceField(choices=ALGO_CHOICES, label="Algoritmo")

    def clean_requests(self):
        raw = self.cleaned_data["requests"] or ""
        # admite "7, 0, 1  2"
        normalized = raw.replace(",", " ").split()
        try:
            reqs = [int(x) for x in normalized]
        except ValueError:
            raise forms.ValidationError("Solo números separados por coma o espacio.")
        if not reqs:
            raise forms.ValidationError("Debes ingresar al menos un número.")
        return reqs

    def clean_algorithm(self):
        # devolvemos el nombre ya normalizado (minúsculas)
        return (self.cleaned_data["algorithm"] or "").strip().lower()

    def to_algo_input(self):
        """Estructura esperada por tus funciones fifo/lru."""
        return {
            "size": self.cleaned_data["size"],
            "requests": self.cleaned_data["requests"],  # ya es lista de ints
        }
