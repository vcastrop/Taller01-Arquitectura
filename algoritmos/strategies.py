from typing import List, Tuple
from .interfaces import DiskSchedulingStrategy
from .fcfs2 import fcfs2
from .sstf import sstf as sstf_fn
from .scan import scan as scan_fn

class FCFSStrategy(DiskSchedulingStrategy):
    def schedule(self, start: int, previous: int, requests: List[int], cylinders: int) -> Tuple[List[int], int]:
        return fcfs2(start, requests)

class SSTFStrategy(DiskSchedulingStrategy):
    def schedule(self, start: int, previous: int, requests: List[int], cylinders: int) -> Tuple[List[int], int]:
        return sstf_fn(start, requests)

class ScanStrategy(DiskSchedulingStrategy):
    def schedule(self, start: int, previous: int, requests: List[int], cylinders: int) -> Tuple[List[int], int]:
        return scan_fn(start, previous, requests, cylinders)
