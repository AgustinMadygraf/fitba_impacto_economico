"""
Path: backend/src/interface_adapter/repositories/producto_repository.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.entities.producto import Producto

class IProductoRepository(ABC):
    @abstractmethod
    def obtener_todos(self) -> List[Producto]:
        pass

    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        pass

    @abstractmethod
    def eliminar(self, producto_id: str) -> None:
        pass
