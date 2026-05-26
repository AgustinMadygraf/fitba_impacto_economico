"""
Path: backend/src/domain/services/servicio_datos_simulacion.py
"""

from typing import List, Dict
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.linea_produccion import LineaProduccion
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada
from src.domain.entities.operacional.oee import OEE
from src.interface_adapter.repositories.json_parametros_repository import JsonParametrosRepository

class ServicioDatosSimulacion:
    def __init__(self, repo: JsonParametrosRepository):
        self.repo = repo

    def obtener_productos_mapeados(self) -> Dict[str, Producto]:
        return {p.sku: p for p in self.repo.get_productos()}

    def obtener_lineas(self) -> List[LineaProduccion]:
        return self.repo.get_lineas()

    def obtener_capacidad(self) -> CapacidadInstalada:
        return self.repo.get_capacidad_instalada()

    def obtener_oee(self) -> OEE:
        return self.repo.get_oee_base()
