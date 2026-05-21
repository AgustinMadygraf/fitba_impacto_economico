"""
Path: src/entities/capacidad_instalada.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class CapacidadInstalada:
    """Representa los límites físicos operativos de la planta."""
    limite_disponibilidad: float
