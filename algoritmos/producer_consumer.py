# algoritmos/producer_consumer.py

import queue
import threading
import time
import random

def simulate_pc(queue_size=100, prod_prio=6.0, cons_prio=2.0, variation=2.0):
    """
    Simula un productor y un consumidor usando hilos,
    y devuelve una lista de líneas (strings) con el log completo.
    """
    # Esta bandera la usan ambos hilos para detenerse
    exit_flag = threading.Event()
    logs = []

    # Compartimos esta cola de tamaño fijo
    q = queue.Queue(maxsize=queue_size)

    # La llenamos a la mitad
    for _ in range(queue_size // 2):
        q.put(1)

    # Productor
    class Producer(threading.Thread):
        def __init__(self, name, priority):
            super().__init__(name=name)
            self.priority = priority
        def run(self):
            logs.append(f"Producer {self.name} started")
            while not exit_flag.is_set():
                time.sleep(self.priority / 10 if self.priority else variation * random.random())
                try:
                    q.put(1, timeout=1)
                    logs.append(f"Producer {self.name} enqueued → size={q.qsize()}")
                except queue.Full:
                    # cola llena: gana productor
                    logs.append("Producer wins (queue full)")
                    exit_flag.set()
            logs.append(f"Producer {self.name} stopped")

    # Consumidor
    class Consumer(threading.Thread):
        def __init__(self, name, priority):
            super().__init__(name=name)
            self.priority = priority
        def run(self):
            logs.append(f"Consumer {self.name} started")
            while not exit_flag.is_set():
                time.sleep(self.priority / 10 if self.priority else variation * random.random())
                try:
                    q.get(timeout=1)
                    logs.append(f"Consumer {self.name} dequeued → size={q.qsize()}")
                except queue.Empty:
                    # cola vacía: gana consumidor
                    logs.append("Consumer wins (queue empty)")
                    exit_flag.set()
            logs.append(f"Consumer {self.name} stopped")

    # Configuramos e iniciamos los hilos
    p = Producer("P1", prod_prio)
    c = Consumer("C1", cons_prio)
    p.start(); c.start()

    # Esperamos a que uno gane
    p.join(); c.join()

    logs.append("Simulation finished")
    return logs
