"""
Path: backend/src/domain/entities/financiero/indice_financiero.py
"""

from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class IndiceFinanciero:
    """
    Representa un índice económico (IPC) con su evolución temporal.
    Entidad responsable de su propia lógica de capitalización.
    """
    nombre: str
    serie_mensual: Dict[int, float]  # Mes (1-based) -> Tasa mensual (ej. 0.04 = 4%)
    tasa_proyectada: float           # Tasa a aplicar si el mes excede la serie disponible

    def calcular_factor_capitalizacion(self, mes: int) -> float:
        """
        Calcula el factor de capitalización compuesta acumulada hasta el mes indicado.
        Formula: F = Product_{i=1 to mes} (1 + tasa_i)
        """
        if mes <= 0:
            return 1.0
            
        factor = 1.0
        for m in range(1, mes + 1):
            tasa = self.serie_mensual.get(m, self.tasa_proyectada)
            factor *= (1 + tasa)
        return factor
