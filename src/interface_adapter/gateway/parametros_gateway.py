from abc import ABC, abstractmethod
from typing import Dict, Any, List
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import MixProduccion
from src.entities.linea_produccion import LineaProduccion
from src.entities.capacidad_instalada import CapacidadInstalada

class ParametrosGateway(ABC):
    """
    Interfaz (Puerto de Entrada de Datos) para obtener la configuración del proyecto.
    Define el contrato para recuperar entidades de dominio desde una fuente externa.
    """

    @abstractmethod
    def get_inversion(self) -> Inversion:
        pass

    @abstractmethod
    def get_productos(self) -> List[Producto]:
        pass

    @abstractmethod
    def get_oee_base(self) -> OEE:
        pass

    @abstractmethod
    def get_lineas_produccion(self) -> List[LineaProduccion]:
        pass

    @abstractmethod
    def get_mix_produccion(self) -> MixProduccion:
        pass

    @abstractmethod
    def get_capacidad_instalada(self) -> CapacidadInstalada:
        pass

    @abstractmethod
    def get_escenarios_raw(self) -> Dict[str, Any]:
        pass
