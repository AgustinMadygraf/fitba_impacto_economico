"""
Path: backend/src/domain/entities/operacional/oee.py
"""

from dataclasses import dataclass
from src.domain.entities.entorno.escenario import Escenario

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
    def evolucionar(self, escenario: Escenario) -> "OEE":
        """Aplica la tasa de crecimiento del escenario a los componentes del OEE."""
        return OEE(
            disponibilidad=self.disponibilidad * (1 + escenario.tasa_disponibilidad),
            rendimiento=self.rendimiento * (1 + escenario.tasa_rendimiento),
            calidad=self.calidad * (1 + escenario.tasa_calidad)
        )

