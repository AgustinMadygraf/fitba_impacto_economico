from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class LineaProduccion:
    """Representa una línea de producción (máquina) y su capacidad."""
    id: str
    nombre: str
    capacidad_nominal: float
    productos_compatibles: List[str]
