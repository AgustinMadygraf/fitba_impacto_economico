from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from src.domain.entities.financiero.inversion import Inversion
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.oee import OEE
from src.domain.entities.operacional.linea_produccion import LineaProduccion
from src.domain.entities.comercial.produccion import MixProduccion
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada

class ParametrosGateway(ABC):
    @abstractmethod
    def get_inversion(self) -> Inversion: pass

    @abstractmethod
    def get_productos(self) -> List[Producto]: pass

    @abstractmethod
    def get_oee_base(self) -> OEE: pass

    @abstractmethod
    def get_lineas_produccion(self) -> List[LineaProduccion]: pass

    @abstractmethod
    def get_mix_produccion(self) -> MixProduccion: pass

    @abstractmethod
    def get_capacidad_instalada(self) -> CapacidadInstalada: pass

    @abstractmethod
    def get_escenarios_raw(self) -> Dict[str, Any]: pass
    
    @abstractmethod
    def get_ipc_override(self) -> Optional[float]: pass
