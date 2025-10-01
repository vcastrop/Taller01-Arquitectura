# common/mixins.py
from typing import Iterable

class PostParamsMixin:
    """Helpers pequeños para leer/validar POST sin reventar."""

    def get_int(self, request, name: str, default=None):
        val = request.POST.get(name, "")
        try:
            return int(val)
        except (TypeError, ValueError):
            return default

    def get_int_list(self, raw: str, sep: Iterable[str] = (",", " ")):
        """Convierte '1,2  3' → [1,2,3]"""
        if raw is None:
            return []
        s = raw
        for sp in sep:
            s = s.replace(sp, " ")
        return [int(x) for x in s.split() if x.strip().isdigit()]
