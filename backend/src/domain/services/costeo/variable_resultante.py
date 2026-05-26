"""
Path: backend/src/domain/services/costeo/variable_resultante.py
"""

from .parametros_costeo import ParametrosCosteo
from .estrategia_costeo import EstrategiaCosteo
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada

class VariableResultante(EstrategiaCosteo):
    """Implementa el costeo variable resultante (solo costos variables)."""
    def calcular_costo_unitario(self, producto: Producto, capacidad: CapacidadInstalada, parametros: ParametrosCosteo) -> float:
        return producto.precio_bobina_kg * (producto.gramaje / 1000)
