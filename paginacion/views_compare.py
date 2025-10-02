from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms_compare import ComparePagingForm
from .services_compare import ComparisonService

class CompareView(FormView):
    template_name = 'paginacion/compare.html'
    form_class = ComparePagingForm
    success_url = reverse_lazy('paginacion:compare')

    def form_valid(self, form):
        data = form.to_algo_input()
        algos = form.cleaned_data["algorithms"]  # ['fifo', 'lru', ...]

        service = ComparisonService()
        result = service.compare(data["size"], data["requests"], algos)
        chart_b64 = service.render_chart_base64(result["chart"])

        context = self.get_context_data(
            form=form,
            comparison=result["rows"],  # lista de {algorithm, metrics:[(name, value), ...]}
            chart_b64=chart_b64
        )
        return self.render_to_response(context)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(
            form=form,
            comparison=None,
            chart_b64=None
        ))
