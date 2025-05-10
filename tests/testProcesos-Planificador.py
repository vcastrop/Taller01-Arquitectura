import pytest
from src.procesos.procesos import Proceso
from src.procesos.planificador import Planificador


def test_creacion_proceso():
    p = Proceso(pid=1, tiempo_llegada=0.0, tiempo_servicio=5.0)
    assert p.pid == 1
    assert p.estado == 'nuevo'
    assert p.tiempo_restante == 5.0


def test_ejecutar_completo():
    p = Proceso(pid=1, tiempo_llegada=0.0, tiempo_servicio=5.0)
    p.ejecutar()
    assert p.tiempo_restante == 0.0
    assert p.estado == 'terminado'


def test_ejecutar_con_quantum():
    p = Proceso(pid=2, tiempo_llegada=0.0, tiempo_servicio=5.0)
    p.ejecutar(quantum=2.0)
    assert p.tiempo_restante == 3.0
    assert p.estado == 'listo'


def test_bloquear_desbloquear():
    p = Proceso(pid=3, tiempo_llegada=0.0, tiempo_servicio=5.0)
    p.bloquear()
    assert p.estado == 'bloqueado'
    p.desbloquear()
    assert p.estado == 'listo'


def test_fcfs_selection():
    p1 = Proceso(pid=1, tiempo_llegada=0.0, tiempo_servicio=4.0)
    p2 = Proceso(pid=2, tiempo_llegada=1.0, tiempo_servicio=3.0)
    plan = Planificador(algoritmo='FCFS')
    plan.agregar_proceso(p1)
    plan.agregar_proceso(p2)

    s1 = plan.seleccionar_siguiente()
    assert s1.pid == 1
    s2 = plan.seleccionar_siguiente()
    assert s2.pid == 2


def test_sjf_selection():
    p1 = Proceso(pid=1, tiempo_llegada=0.0, tiempo_servicio=4.0)
    p2 = Proceso(pid=2, tiempo_llegada=1.0, tiempo_servicio=3.0)
    p3 = Proceso(pid=3, tiempo_llegada=2.0, tiempo_servicio=5.0)
    plan = Planificador(algoritmo='SJF')
    plan.agregar_proceso(p1)
    plan.agregar_proceso(p2)
    plan.agregar_proceso(p3)

    # El primer seleccionado debe ser p2 (3 < 4 < 5)
    s1 = plan.seleccionar_siguiente()
    assert s1.pid == 2
    # Luego p1 (4), luego p3 (5)
    s2 = plan.seleccionar_siguiente()
    assert s2.pid == 1
    s3 = plan.seleccionar_siguiente()
    assert s3.pid == 3