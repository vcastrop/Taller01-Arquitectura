# algoritmos/factory.py

# algoritmos/factory.py

def _norm(name: str) -> str:
    return (name or "").strip().lower()

# ---------------- CPU ----------------
from .fcfs import fcfs
try:
    # tu archivo es RR.py (con mayúsculas)
    from .RR import rr
except ImportError:
    # por si en algún entorno el archivo es rr.py
    from .rr import rr  # noqa

_CPU = {
    "fcfs": fcfs,
    "rr": rr,
}

def get_cpu_scheduler(name: str):
    key = _norm(name)
    if key not in _CPU:
        raise ValueError(f"Algoritmo de CPU desconocido: {name}")
    return _CPU[key]

# ------------- Paginación -------------
from .fifo import fifo
from .lru import lru

_PAGE = {
    "fifo": fifo,
    "lru": lru,
}

def get_page_replacement(name: str):
    key = _norm(name)
    if key not in _PAGE:
        raise ValueError(f"Algoritmo de paginación desconocido: {name}")
    return _PAGE[key]

# --------------- Disco ----------------
from .fcfs2 import fcfs2
from .sstf import sstf
from .scan import scan

_DISK = {
    "fcfs": fcfs2,   # tu implementación de FCFS para disco está en fcfs2.py
    "sstf": sstf,
    "scan": scan,
}

def get_disk_scheduler(name: str):
    key = _norm(name)
    if key not in _DISK:
        raise ValueError(f"Algoritmo de disco desconocido: {name}")
    return _DISK[key]
