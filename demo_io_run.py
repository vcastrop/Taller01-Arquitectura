from src.procesos.procesos import Proceso
from src.procesos.planificador import Planificador


def main():
    # Definimos tres procesos con llegada y tiempo de servicio
    procesos = [
        Proceso(pid=1, tiempo_llegada=0, tiempo_servicio=6),
        Proceso(pid=2, tiempo_llegada=1, tiempo_servicio=4),
        Proceso(pid=3, tiempo_llegada=2, tiempo_servicio=5),
    ]
    # Configuramos que el proceso 2 realice I/O después de usar 2 unidades de CPU
    io_block_times = {2: 2}
    io_duration = 3
    io_done = set()  # Para que la petición de I/O solo ocurra una vez por proceso

    plan = Planificador(algoritmo='FCFS')
    pendientes = procesos.copy()
    bloqueados = []  # lista de tuplas (proceso, tiempo_desbloqueo)
    completados = []
    tiempo = 0

    print("=== Demo I/O con FCFS ===\n")
    while len(completados) < len(procesos):
        # 1. Llegada de nuevos procesos
        for p in pendientes[:]:
            if p.tiempo_llegada <= tiempo:
                print(f"t={tiempo}: Llega proceso {p.pid}")
                plan.agregar_proceso(p)
                pendientes.remove(p)

        # 2. Desbloqueo tras I/O completado
        for p, t_desbloqueo in bloqueados[:]:
            if tiempo >= t_desbloqueo:
                p.desbloquear()
                print(f"t={tiempo}: I/O completado para proceso {p.pid}, vuelve a lista")
                plan.agregar_proceso(p)
                bloqueados.remove((p, t_desbloqueo))

        # 3. Planificación y ejecución
        proc = plan.planificar(tiempo)
        if proc:
            print(f"t={tiempo}: Ejecutando proceso {proc.pid} (restante={proc.tiempo_restante})")
            # ¿Debe hacer I/O y aún no lo ha hecho?
            if proc.pid in io_block_times and proc.pid not in io_done and proc.tiempo_restante > io_block_times[proc.pid]:
                # Ejecutamos solo hasta el punto de I/O
                run_time = io_block_times[proc.pid]
                proc.ejecutar(quantum=run_time)
                tiempo += run_time
                print(f"t={tiempo}: Proceso {proc.pid} solicita I/O y se bloquea")
                proc.bloquear()
                # Se desbloqueará después de la duración de I/O
                bloqueados.append((proc, tiempo + io_duration))
                io_done.add(proc.pid)
            else:
                # Ejecutar hasta terminar el restante
                prev_rem = proc.tiempo_restante
                proc.ejecutar()
                tiempo += prev_rem
                if proc.estado == 'terminado':
                    print(f"t={tiempo}: Proceso {proc.pid} terminado")
                    completados.append(proc)
                else:
                    # Si quedó listo (por si no alcanzó a terminar), lo reencolamos
                    print(f"t={tiempo}: Proceso {proc.pid} vuelve a lista (restante={proc.tiempo_restante})")
                    plan.agregar_proceso(proc)
            print()
        else:
            # CPU inactiva: avanzar al siguiente evento (llegada o desbloqueo)
            tiempos_evento = []
            if pendientes:
                tiempos_evento.append(min(p.tiempo_llegada for p in pendientes))
            if bloqueados:
                tiempos_evento.append(min(t for (_, t) in bloqueados))
            if not tiempos_evento:
                break
            siguiente = min(tiempos_evento)
            print(f"t={tiempo}: CPU inactiva, avanzando a t={siguiente}\n")
            tiempo = siguiente

if __name__ == '__main__':
    main()