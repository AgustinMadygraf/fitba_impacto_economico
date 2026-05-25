from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada
from src.domain.entities.operacional.oee import OEE
from src.domain.entities.entorno.escenario import Escenario

class CalculadorImpactoOperativo:
    @staticmethod
    def calcular_volumenes(disponibilidad_t: float, oee_base: OEE, capacidad_instalada: CapacidadInstalada, escenario: Escenario) -> tuple[float, float]:
        oee_t = disponibilidad_t * oee_base.rendimiento * oee_base.calidad
        volumen_produccion = capacidad_instalada.capacidad_nominal_total * min(oee_t, 1.0)
        volumen_ventas = volumen_produccion * escenario.factor_demanda
        return volumen_produccion, volumen_ventas
