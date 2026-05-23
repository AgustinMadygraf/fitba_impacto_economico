""" Path: src/entities/oee.py """
from dataclasses import dataclass

@dataclass(frozen=True)
class OEE:
    """Representa los componentes del OEE (Disponibilidad, Rendimiento, Calidad)."""
    disponibilidad: float
    rendimiento: float
    calidad: float

    @property
    def valor(self) -> float:
        """Calcula el valor del OEE como producto de sus factores."""
        return self.disponibilidad * self.rendimiento * self.calidad
