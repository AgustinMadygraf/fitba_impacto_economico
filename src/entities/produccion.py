"""
Path: src/entities/produccion.py
"""

from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Produccion:
    """
    Representa los parámetros operativos de producción.
    El volumen de producción se modela como un vector para la proyección mensual.
    """
    volumen_base: float
    volumen_vector: List[float]
