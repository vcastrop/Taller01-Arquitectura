# algoritmos/dining.py

def simulate_dining(num_philosophers, iterations=1):
    """
    Simula de forma secuencial el algoritmo de Cena de los Filósofos.
    Devuelve una lista de cadenas con el log paso a paso.
    """
    LEFT = lambda i: (i - 1 + num_philosophers) % num_philosophers
    RIGHT = lambda i: (i + 1) % num_philosophers

    # 0 = thinking, 1 = hungry, 2 = eating
    state = [0] * num_philosophers
    logs = []

    for it in range(iterations):
        logs.append(f"--- Iteration {it+1} ---")
        for i in range(num_philosophers):
            logs.append(f"Philosopher {i} is thinking")
            logs.append(f"Philosopher {i} is hungry")

            # compruebo si puede comer
            if state[LEFT(i)] != 2 and state[RIGHT(i)] != 2:
                state[i] = 2
                logs.append(f"Philosopher {i} picks up forks and starts eating")
                logs.append(f"Philosopher {i} finishes eating and puts down forks")
                state[i] = 0
                # despierto a vecinos
                logs.append(f"Philosopher {i} signals {LEFT(i)} and {RIGHT(i)}")
            else:
                logs.append(f"Philosopher {i} cannot eat (neighbor eating)")

    return logs
