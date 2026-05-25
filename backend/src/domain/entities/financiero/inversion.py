"""
Path: backend/src/entities/inversion.py
"""

from dataclasses import dataclass
from typing import Optional
from src.domain.entities.financiero.indice_financiero import IndiceFinanciero

@dataclass(frozen=True)
class Inversion:
    monto_anr: float
    fecha_base: str
    indice_base: Optional[IndiceFinanciero] = None

    @property
    def monto_actualizado(self) -> float:
        return self.monto_anr

    def calcular_target_proyectado(self, mes: int) -> float:
        if not self.indice_base:
            return self.monto_anr
        return self.monto_anr * self.indice_base.calcular_factor_capitalizacion(mes)
