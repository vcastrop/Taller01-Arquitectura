class Proceso:
    """
    Representa un proceso del sistema operativo.
    Atributos:
        pid: int
        estado: str       # 'nuevo', 'listo', 'ejecutando', 'bloqueado', 'terminado'
        tiempo_llegada: float
        tiempo_servicio: float
        tiempo_restante: float
    """
    def __init__(self, pid: int, tiempo_llegada: float, tiempo_servicio: float):
        self.pid = pid
        self.tiempo_llegada = tiempo_llegada
        self.tiempo_servicio = tiempo_servicio
        self.tiempo_restante = tiempo_servicio
        self.estado = 'nuevo'

    def ejecutar(self, quantum: float = None) -> None:
        """
        Ejecuta el proceso durante un quantum (si aplica) o hasta completarse.
        Actualiza `tiempo_restante` y `estado`.
        """
        self.estado = 'ejecutando'
        if quantum is None:
            # Ejecuta hasta terminar
            self.tiempo_restante = 0.0
        else:
            # Ejecuta solo durante el quantum
            tiempo_ejecutado = min(quantum, self.tiempo_restante)
            self.tiempo_restante -= tiempo_ejecutado
        if self.tiempo_restante <= 0:
            self.tiempo_restante = 0.0
            self.estado = 'terminado'
        else:
            self.estado = 'listo'

    def bloquear(self) -> None:
        """Cambia el estado a 'bloqueado'."""
        self.estado = 'bloqueado'

    def desbloquear(self) -> None:
        """Cambia el estado a 'listo'."""
        self.estado = 'listo'