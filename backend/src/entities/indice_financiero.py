from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class IndiceFinanciero:
    """Representa un índice económico (IPC, Dólar, etc.) con su evolución temporal."""
    nombre: str
    serie_mensual: Dict[int, float]  # Mes -> Tasa mensual (0.04 = 4%)
    tasa_proyectada: float          # Tasa a aplicar si el mes excede la serie

    def obtener_factor_acumulado(self, mes_objetivo: int) -> float:
        """
        Calcula el factor de capitalización compuesta hasta el mes indicado.
        Factor = (1 + r1) * (1 + r2) * ... * (1 + rn)
        """
        factor = 1.0
        for m in range(1, mes_objetivo + 1):
            tasa = self.serie_mensual.get(m, self.tasa_proyectada)
            factor *= (1 + tasa)
        return factor
