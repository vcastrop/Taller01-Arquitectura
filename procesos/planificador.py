from collections import deque
import heapq
from procesos.procesos import Proceso

from collections import deque

class RoundRobin:
    def __init__(self, quantum):
        self.quantum = quantum
        self.cola = deque()
        self.suspendidos = []

    def agregar(self, proceso):
        if proceso.estado == 'suspendido':
            proceso.reanudar()
        else:
            proceso.cambiar_estado('listo')
        self.cola.append(proceso)

    def suspender_proceso(self, pid):
        for proceso in list(self.cola):  # convertimos a lista para evitar errores al modificar
            if proceso.pid == pid:
                proceso.suspender()
                self.suspendidos.append(proceso)
                self.cola.remove(proceso)
                return
        print(f"⚠️ Proceso con PID={pid} no encontrado o no suspendible.")

    def ejecutar(self):
        print("\n[Round Robin]")
        while self.cola:
            p = self.cola.popleft()
            if p.estado != 'suspendido':
                terminado = p.ejecutar(self.quantum)
                if not terminado:
                    self.cola.append(p)



class SJF:
    def __init__(self):
        self.cola = []

    def agregar(self, proceso):
        proceso.cambiar_estado('listo')
        heapq.heappush(self.cola, (proceso.duracion, proceso))

    def ejecutar(self):
        print("\n[SJF]")
        while self.cola:
            _, p = heapq.heappop(self.cola)
            p.ejecutar()
