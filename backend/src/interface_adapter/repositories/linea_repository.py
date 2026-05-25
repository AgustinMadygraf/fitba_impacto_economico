"""
Path: backend/src/interface_adapter/repositories/linea_repository.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.operacional.linea_produccion import LineaProduccion

class ILineaProduccionRepository(ABC):
    @abstractmethod
    def obtener_todos(self) -> List[LineaProduccion]:
        pass

    @abstractmethod
    def guardar(self, linea: LineaProduccion) -> None:
        pass

    @abstractmethod
    def eliminar(self, linea_id: str) -> None:
        pass
