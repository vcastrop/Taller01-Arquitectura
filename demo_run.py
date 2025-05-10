import argparse
from src.procesos.procesos import Proceso
from src.procesos.planificador import Planificador


def simulate(algoritmo: str):
    procesos = [
        Proceso(pid=1, tiempo_llegada=0, tiempo_servicio=5),
        Proceso(pid=2, tiempo_llegada=5, tiempo_servicio=3),
        Proceso(pid=3, tiempo_llegada=5, tiempo_servicio=8),
        Proceso(pid=4, tiempo_llegada=8, tiempo_servicio=6),
    ]
    plan = Planificador(algoritmo=algoritmo)
    pendientes = procesos.copy()
    tiempo = 0
    completados = []

    print(f"=== Simulación {plan.algoritmo} ===")
    while len(completados) < len(procesos):
        # Llegadas
        for p in pendientes[:]:
            if p.tiempo_llegada <= tiempo:
                print(f"t={tiempo}: Llega proceso {p.pid} (servicio={p.tiempo_servicio})")
                plan.agregar_proceso(p)
                pendientes.remove(p)

        proc = plan.planificar(tiempo)
        if proc:
            print(f"t={tiempo}: Ejecutando proceso {proc.pid} (restante={proc.tiempo_restante})")
            # Ejecutar sin quantum para no preemptivo
            proc.ejecutar()
            tiempo += proc.tiempo_servicio
            print(f"t={tiempo}: Proceso {proc.pid} terminado")
            completados.append(proc)
        else:
            print(f"t={tiempo}: CPU inactiva")
            # Avanzar al siguiente evento de llegada si existe
            if pendientes:
                tiempo_siguiente = min(p.tiempo_llegada for p in pendientes)
                tiempo = tiempo_siguiente
            else:
                break


def main():
    parser = argparse.ArgumentParser(description='Demo de planificación de procesos')
    parser.add_argument('-a', '--algoritmo', choices=['FCFS', 'SJF'], default='FCFS',
                        help='Algoritmo de planificación (FCFS o SJF)')
    args = parser.parse_args()
    simulate(args.algoritmo)


if __name__ == '__main__':
    main()
