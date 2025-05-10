from procesos import Proceso, RoundRobin, SJF

def crear_procesos():
    return [
        Proceso("Proceso1", duracion=6),
        Proceso("Proceso2", duracion=4),
        Proceso("Proceso3", duracion=8)
    ]

def demo_round_robin():
    print("\n===== DEMO ROUND ROBIN =====")
    procesos = crear_procesos()
    rr = RoundRobin(quantum=3)
    for p in procesos:
        rr.agregar(p)
    rr.ejecutar()

def demo_sjf():
    print("\n===== DEMO SJF (Shortest Job First) =====")
    procesos = crear_procesos()
    sjf = SJF()
    for p in procesos:
        sjf.agregar(p)
    sjf.ejecutar()

def demo_suspension():
    print("\n===== DEMO SUSPENSIÓN Y REANUDACIÓN =====")
    p1 = Proceso("Proceso1", duracion=6)
    p2 = Proceso("Proceso2", duracion=5)

    rr = RoundRobin(quantum=3)
    rr.agregar(p1)
    rr.agregar(p2)

    # Ejecutar un turno
    rr.ejecutar()  # se ejecuta una vez por cada proceso

    # Simular suspensión de p2
    rr.suspender_proceso(p2.pid)

    # Ejecutar lo restante (solo p1 debería continuar)
    rr.ejecutar()

    # Reanudar p2 y volver a agregarlo
    rr.agregar(p2)

    # Ejecutar lo que queda
    rr.ejecutar()

if __name__ == "__main__":
    demo_suspension()


if __name__ == "__main__":
    demo_round_robin()
    demo_sjf()
