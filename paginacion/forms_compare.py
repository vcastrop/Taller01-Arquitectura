from django import forms

ALGO_CHOICES = (
    ("FIFO", "FIFO"),
    ("LRU",  "LRU"),
)

class ComparePagingForm(forms.Form):
    size = forms.IntegerField(min_value=1, label="Tamaño de marcos")
    requests = forms.CharField(label="Secuencia (coma o espacio)")
    algorithms = forms.MultipleChoiceField(
        choices=ALGO_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Algoritmos a comparar",
    )

    def clean_requests(self):
        raw = self.cleaned_data.get("requests") or ""
        parts = raw.replace(",", " ").split()
        try:
            nums = [int(x) for x in parts]
        except ValueError:
            raise forms.ValidationError("Solo números separados por coma/espacio.")
        if not nums:
            raise forms.ValidationError("Ingresa al menos un número.")
        return nums

    def clean_algorithms(self):
        algos = self.cleaned_data.get("algorithms") or []
        norm = [(a or "").strip().lower() for a in algos]
        if not norm:
            raise forms.ValidationError("Selecciona al menos un algoritmo.")
        return norm

    def to_algo_input(self):
        return {
            "size": self.cleaned_data["size"],
            "requests": self.cleaned_data["requests"],  # ya es lista de ints
        }
