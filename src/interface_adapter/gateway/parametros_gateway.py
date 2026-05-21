"""
Path: src/interface_adapter/gateway/parametros_gateway.py
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import Produccion
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
    def get_producto(self) -> Producto:
        pass

    @abstractmethod
    def get_oee_base(self) -> OEE:
        pass

    @abstractmethod
    def get_produccion_base(self) -> Produccion:
        pass

    @abstractmethod
    def get_capacidad_instalada(self) -> CapacidadInstalada:
        pass

    @abstractmethod
    def get_escenarios_raw(self) -> Dict[str, Any]:
        pass
