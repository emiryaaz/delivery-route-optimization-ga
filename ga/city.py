from dataclasses import dataclass
import math


@dataclass
class City:
    id: int
    x: float
    y: float

    def distance_to(self, other: "City") -> float:
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
