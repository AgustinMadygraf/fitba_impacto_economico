"""
Path: backend/src/domain/services/costeo/variable_normalizado.py
"""

from .parametros_costeo import ParametrosCosteo
from .estrategia_costeo import EstrategiaCosteo
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada

class VariableNormalizado(EstrategiaCosteo):
    """Implementa costeo variable normalizado (variable + CIF variables absorbidos por capacidad normal)."""
    def calcular_costo_unitario(self, producto: Producto, capacidad: CapacidadInstalada, parametros: ParametrosCosteo) -> float:
        costo_variable = producto.precio_bobina_kg * (producto.gramaje / 1000)
        cif_variables = parametros.cif_variables_totales
        return costo_variable + (cif_variables / capacidad.capacidad_normal_mensual)
