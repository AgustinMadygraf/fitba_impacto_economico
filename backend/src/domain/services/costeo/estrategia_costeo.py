"""
Path: backend/src/domain/services/costeo/estrategia_costeo.py
"""

from abc import ABC, abstractmethod
from typing import Dict
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada

class EstrategiaCosteo(ABC):
    """Interfaz base para las estrategias de cálculo de costos."""

    @abstractmethod
    def calcular_costo_unitario(
        self,
        producto: Producto,
        capacidad: CapacidadInstalada,
        datos_financieros: Dict
    ) -> float:
        """Calcula el costo unitario según la estrategia específica."""
        pass
