"""
Path: src/entities/inversion.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Inversion:
    """Representa la inversión inicial del ANR y su actualización financiera."""
    monto_anr: float
    factor_ipc: float

    @property
    def monto_actualizado(self) -> float:
        """Calcula el monto de la inversión actualizado por el factor IPC."""
        return self.monto_anr * self.factor_ipc
