import uuid
import time

class Proceso:
    def __init__(self, nombre, duracion):
        self.pid = str(uuid.uuid4())[:8]
        self.nombre = nombre
        self.duracion = duracion  # Tiempo total estimado
        self.restante = duracion  # Tiempo que le falta
        self.estado = 'nuevo'

    def cambiar_estado(self, nuevo_estado):
        print(f"Proceso {self.nombre} (PID={self.pid}): {self.estado} → {nuevo_estado}")
        self.estado = nuevo_estado

    def ejecutar(self, quantum=None):
        self.cambiar_estado('ejecutando')
        if quantum:
            tiempo = min(quantum, self.restante)
        else:
            tiempo = self.restante
        print(f"    Ejecutando {self.nombre} por {tiempo} unidades")
        time.sleep(0.1)  # Simula ejecución
        self.restante -= tiempo

        if self.restante > 0:
            self.cambiar_estado('listo')
            return False  # No ha terminado
        else:
            self.cambiar_estado('terminado')
            return True  # Ya terminó

    def suspender(self):
        if self.estado in ['listo', 'ejecutando']:
            self.cambiar_estado('suspendido')
        else:
            print(f"⚠️  No se puede suspender el proceso {self.nombre} en estado '{self.estado}'")

    def reanudar(self):
        if self.estado == 'suspendido':
            self.cambiar_estado('listo')
        else:
            print(f"⚠️  No se puede reanudar el proceso {self.nombre} en estado '{self.estado}'")

