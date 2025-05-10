from collections import deque

class FIFO:
    def __init__(self):
        self.cola = deque()

    def referencia(self, marco):
        self.cola.append(marco)

    def reemplazar(self):
        if self.cola:
            return self.cola.popleft()
        return None

    def eliminar(self, marco):
        if marco in self.cola:
            self.cola.remove(marco)


class LRU:
    def __init__(self):
        self.uso_reciente = []

    def referencia(self, marco):
        if marco in self.uso_reciente:
            self.uso_reciente.remove(marco)
        self.uso_reciente.append(marco)

    def reemplazar(self):
        if self.uso_reciente:
            return self.uso_reciente.pop(0)
        return None

    def eliminar(self, marco):
        if marco in self.uso_reciente:
            self.uso_reciente.remove(marco)
