"""
Path: backend/src/domain/services/costeo/completo_normalizado_integral.py
"""

from .parametros_costeo import ParametrosCosteo
from .estrategia_costeo import EstrategiaCosteo
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada

class CompletoNormalizadoIntegral(EstrategiaCosteo):
    """Implementa costeo completo normalizado integral (variable + CIF fijos absorbidos por capacidad normal)."""
    def calcular_costo_unitario(self, producto: Producto, capacidad: CapacidadInstalada, parametros: ParametrosCosteo) -> float:
        costo_variable = producto.precio_bobina_kg * (producto.gramaje / 1000)
        cif_fijos = parametros.cif_fijos_totales
        return costo_variable + (cif_fijos / capacidad.capacidad_normal_mensual)
