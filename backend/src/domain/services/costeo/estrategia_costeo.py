from abc import ABC, abstractmethod
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada
from .parametros_costeo import ParametrosCosteo

class EstrategiaCosteo(ABC):
    """Interfaz base para las estrategias de cálculo de costos."""

    @abstractmethod
    def calcular_costo_unitario(
        self,
        producto: Producto,
        capacidad: CapacidadInstalada,
        parametros: ParametrosCosteo
    ) -> float:
        """Calcula el costo unitario según la estrategia específica."""
        pass
