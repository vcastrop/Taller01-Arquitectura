class PageResultAdapter:
    """
    Normaliza la salida de FIFO/LRU a un esquema común de métricas.
    Soporta claves 'hit_ratio' o 'hit-ratio', y opcionalmente 'hits'/'faults'.
    Devuelve: dict con keys estándar y lista de métricas para pintar.
    """
    @staticmethod
    def normalize(result: dict) -> dict:
        if not isinstance(result, dict):
            return {}

        # Normalizar 'hit_ratio'
        if "hit_ratio" in result:
            hit_ratio = result["hit_ratio"]
        elif "hit-ratio" in result:
            hit_ratio = result["hit-ratio"]
        else:
            hit_ratio = None

        hits = result.get("hits")
        faults = result.get("faults")

        return {
            "hit_ratio": hit_ratio,
            "hits": hits,
            "faults": faults,
        }

    @staticmethod
    def to_metrics(nrom: dict):
        """
        Convierte el dict normalizado en lista de métricas [(name, value)].
        Solo incluye métricas disponibles.
        """
        out = []
        if nrom.get("hit_ratio") is not None:
            out.append(("hit_ratio", nrom["hit_ratio"]))
        if nrom.get("hits") is not None:
            out.append(("hits", nrom["hits"]))
        if nrom.get("faults") is not None:
            out.append(("faults", nrom["faults"]))
        return out
