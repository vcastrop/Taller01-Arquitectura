from typing import Dict
from algoritmos.interfaces import DiskSchedulingStrategy

class DiskSchedulerService:
    def __init__(self, strategies: Dict[str, DiskSchedulingStrategy]):
        self._strategies = strategies

    def run(self, key: str, start: int, previous: int, requests, cylinders: int):
        try:
            strategy = self._strategies[key]
        except KeyError:
            raise ValueError(f"Algoritmo no soportado: {key}")
        return strategy.schedule(start, previous, requests, cylinders)
