import random


def simulate_pc_sync(queue_size=20, prod_prio=6.0, cons_prio=2.0, variation=2.0, max_steps=100):
    logs = []
    # Empezamos la cola a la mitad
    count = queue_size // 2
    logs.append(f"Initial queue size = {count}")

    # Proporción de probabilidad de producir vs consumir
    p_prod = prod_prio / (prod_prio + cons_prio)

    for step in range(1, max_steps + 1):
        # Decidimos si producimos o consumimos
        if random.random() < p_prod:
            # intento producir
            if count < queue_size:
                count += 1
                logs.append(f"[{step}] Produce → size={count}")
            else:
                logs.append(f"[{step}] Producer wins (queue full at {count})")
                break
        else:
            # intento consumir
            if count > 0:
                count -= 1
                logs.append(f"[{step}] Consume  → size={count}")
            else:
                logs.append(f"[{step}] Consumer wins (queue empty)")
                break
    else:
        logs.append(f"Reached max_steps={max_steps} without finish")

    logs.append("Simulation ended")
    return logs
