from dataclasses import dataclass
from typing import Optional
from src.entities.indice_financiero import IndiceFinanciero

@dataclass(frozen=True)
class Inversion:
    """Representa la inversión inicial del ANR y su actualización financiera."""
    monto_anr: float
    indice_base: Optional[IndiceFinanciero] = None
    factor_correccion_inicial: float = 1.0

    @property
    def monto_actualizado(self) -> float:
        """
        Calcula el monto de la inversión actualizado al 'Día 0' de la simulación.
        Esto considera la inflación ocurrida entre el otorgamiento y el inicio.
        """
        return self.monto_anr * self.factor_correccion_inicial

    def calcular_target_proyectado(self, mes: int) -> float:
        """
        Calcula el valor nominal que tendrá el target de repago en el mes N
        aplicando la capitalización compuesta del índice.
        """
        if not self.indice_base:
            return self.monto_actualizado
            
        return self.monto_actualizado * self.indice_base.calcular_factor_capitalizacion(mes)
