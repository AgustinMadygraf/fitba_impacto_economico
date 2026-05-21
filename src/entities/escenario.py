"""
Path: src/entities/escenario.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Escenario:
    """Representa los parámetros variables de un escenario de simulación."""
    nombre: str
    tasa_crecimiento: float
    factor_demanda: float
