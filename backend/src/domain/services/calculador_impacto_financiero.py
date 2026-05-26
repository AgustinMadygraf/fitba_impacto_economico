"""
Path: backend/src/domain/services/calculador_impacto_financiero.py
"""

from datetime import datetime
from src.domain.services.costeo.estrategia_costeo import EstrategiaCosteo
from src.domain.services.costeo.parametros_costeo import ParametrosCosteo
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada
from src.domain.entities.financiero.inversion import Inversion
from src.domain.entities.financiero.indice_financiero import IndiceFinanciero
from src.domain.services.calculador_ipc import CalculadorIPC

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

    def calcular_costo_unitario(
        self,
        estrategia: EstrategiaCosteo,
        producto: Producto,
        capacidad: CapacidadInstalada,
        parametros: ParametrosCosteo
    ) -> float:
        return estrategia.calcular_costo_unitario(producto, capacidad, parametros)

