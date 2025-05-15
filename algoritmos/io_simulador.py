
import threading
import time
import random

class ImpresoraCompartida:
    def __init__(self):
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.ocupada = False
        self.log = []

    def solicitar_acceso(self, empleado_id):
        with self.condition:
            self.log.append(f"Empleado {empleado_id} está esperando para imprimir. (Fase crítica)")
            while self.ocupada:
                self.condition.wait()
            self.ocupada = True
            self.log.append(f"Empleado {empleado_id} está imprimiendo... (Fase protegida)")

    def liberar_acceso(self, empleado_id):
        with self.condition:
            self.log.append(f"Empleado {empleado_id} ha terminado de imprimir.")
            self.ocupada = False
            self.condition.notify()


def simular_empleados_con_impresora(empleados):
    impresora = ImpresoraCompartida()
    threads = []

    def empleado_func(emp):
        # Fase de espera
        espera = random.uniform(0.5, 2.0)
        impresora.log.append(f"Empleado {emp['id']} está preparando su documento... (Fase de espera: {espera:.1f}s)")
        time.sleep(espera)

        # Fase crítica y protegida
        impresora.solicitar_acceso(emp['id'])
        time.sleep(emp['duracion'])
        impresora.liberar_acceso(emp['id'])

    for emp in empleados:
        t = threading.Thread(target=empleado_func, args=(emp,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return impresora.log