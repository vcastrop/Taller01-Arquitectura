from abc import ABC, abstractmethod
from typing import List, Tuple

class DiskSchedulingStrategy(ABC):
    @abstractmethod
    def schedule(
        self, start: int, previous: int, requests: List[int], cylinders: int
    ) -> Tuple[List[int], int]:
        ...
