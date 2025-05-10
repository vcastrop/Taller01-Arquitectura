from typing import List, Optional
from src.procesos.procesos import Proceso

class Planificador:
    """
    Planificador de CPU genérico.
    Permite implementar diferentes algoritmos (FCFS, SJF, RR, etc.).
    """
    def __init__(self, algoritmo: str = 'FCFS'):
        self.cola_listos: List[Proceso] = []
        self.algoritmo = algoritmo.upper()

    def agregar_proceso(self, proceso: Proceso) -> None:
        """Agrega un proceso a la cola de listos y actualiza su estado a 'listo'."""
        proceso.estado = 'listo'
        self.cola_listos.append(proceso)

    def eliminar_proceso(self, pid: int) -> None:
        """Elimina un proceso de la cola de listos por su PID."""
        self.cola_listos = [p for p in self.cola_listos if p.pid != pid]

    def seleccionar_siguiente(self) -> Optional[Proceso]:
        """
        Elige el siguiente proceso a ejecutar según el algoritmo configurado:
        - FCFS: el primer proceso en la cola
        - SJF: proceso con menor tiempo de servicio
        """
        if not self.cola_listos:
            return None
        if self.algoritmo == 'SJF':
            # No preemptive SJF: elegir por tiempo de servicio
            siguiente = min(self.cola_listos, key=lambda p: p.tiempo_servicio)
            self.cola_listos.remove(siguiente)
        else:
            # FCFS por defecto
            siguiente = self.cola_listos.pop(0)
        siguiente.estado = 'ejecutando'
        return siguiente

    def planificar(self, tiempo_actual: float) -> Optional[Proceso]:
        """
        Punto de entrada para el planificador:
        - (Ignora `tiempo_actual` en algoritmos no preemptivos)
        - Llama a `seleccionar_siguiente`.
        - Retorna proceso a ejecutar.
        """
        return self.seleccionar_siguiente()