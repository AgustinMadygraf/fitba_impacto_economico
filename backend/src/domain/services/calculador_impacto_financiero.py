from datetime import datetime
from src.domain.entities.financiero.inversion import Inversion
from src.domain.entities.financiero.indice_financiero import IndiceFinanciero
from src.application.calculador_ipc import CalculadorIPC

class CalculadorImpactoFinanciero:
    @staticmethod
    def calcular_inflacion(inversion: Inversion, indice_base: IndiceFinanciero | None, fecha_actual: datetime) -> tuple[float, float]:
        factor_inflacion = 1.0
        if indice_base:
            factor_inflacion = CalculadorIPC.calculate_factor(indice_base, inversion.fecha_base, fecha_actual)
            target_actualizado = inversion.monto_anr * factor_inflacion
        else:
            target_actualizado = inversion.monto_anr
        return factor_inflacion, target_actualizado
