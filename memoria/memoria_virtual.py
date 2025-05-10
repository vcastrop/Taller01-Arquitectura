class MemoriaVirtual:
    def __init__(self, marcos_totales):
        self.marcos_totales = marcos_totales
        self.marcos = [None] * marcos_totales  # Cada marco: (pid, num_pagina)
        self.tablas_paginas = {}  # pid -> {num_pagina: num_marco}
        self.fallos_pagina = {}   # pid -> cantidad

    def crear_proceso(self, pid, paginas):
        self.tablas_paginas[pid] = {i: None for i in range(paginas)}
        self.fallos_pagina[pid] = 0
        print(f"🔧 Proceso {pid} creado con {paginas} páginas.")

    def acceder_pagina(self, pid, num_pagina):
        tabla = self.tablas_paginas.get(pid)
        if tabla is None:
            print(f"❌ El proceso {pid} no existe.")
            return

        marco = tabla.get(num_pagina)
        if marco is not None:
            print(f"✅ Página {num_pagina} del proceso {pid} ya está en el marco {marco}.")
            return

        # Fallo de página
        print(f"⚠️ Fallo de página: Proceso {pid}, página {num_pagina}")
        self.fallos_pagina[pid] += 1
        self.cargar_pagina(pid, num_pagina)

    def cargar_pagina(self, pid, num_pagina):
        # Buscar marco libre
        for i, contenido in enumerate(self.marcos):
            if contenido is None:
                self.marcos[i] = (pid, num_pagina)
                self.tablas_paginas[pid][num_pagina] = i
                print(f"📥 Página {num_pagina} de {pid} cargada en marco {i}.")
                return

        print("❌ No hay marcos libres. Se necesita reemplazo (próxima fase).")

    def estado_memoria(self):
        print("\n📊 Estado actual de los marcos:")
        for i, contenido in enumerate(self.marcos):
            if contenido is None:
                print(f"  Marco {i}: libre")
            else:
                pid, pag = contenido
                print(f"  Marco {i}: Proceso {pid}, Página {pag}")

    def estadisticas(self):
        print("\n📈 Fallos de página por proceso:")
        for pid, fallos in self.fallos_pagina.items():
            print(f"  {pid}: {fallos} fallos")


from memoria.algoritmos import FIFO, LRU

class MemoriaVirtual:
    def __init__(self, marcos_totales, algoritmo="FIFO"):
        self.marcos_totales = marcos_totales
        self.marcos = [None] * marcos_totales
        self.tablas_paginas = {}
        self.fallos_pagina = {}

        if algoritmo == "FIFO":
            self.algoritmo = FIFO()
        elif algoritmo == "LRU":
            self.algoritmo = LRU()
        else:
            raise ValueError("Algoritmo no soportado")

    def cargar_pagina(self, pid, num_pagina):
        marco_liberado = None
        for i, contenido in enumerate(self.marcos):
            if contenido is None:
                self.marcos[i] = (pid, num_pagina)
                self.tablas_paginas[pid][num_pagina] = i
                self.algoritmo.referencia(i)
                return

        # Si no hay marcos libres → usar algoritmo de reemplazo
        marco_reemplazo = self.algoritmo.reemplazar()
        if marco_reemplazo is not None:
            proceso_ant, pagina_ant = self.marcos[marco_reemplazo]
            self.tablas_paginas[proceso_ant][pagina_ant] = None
            self.marcos[marco_reemplazo] = (pid, num_pagina)
            self.tablas_paginas[pid][num_pagina] = marco_reemplazo
            self.algoritmo.referencia(marco_reemplazo)
