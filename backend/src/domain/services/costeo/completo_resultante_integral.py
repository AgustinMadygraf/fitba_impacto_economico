"""
Path: backend/src/domain/services/costeo/completo_resultante_integral.py
"""

from .parametros_costeo import ParametrosCosteo
from .estrategia_costeo import EstrategiaCosteo
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada

class CompletoResultanteIntegral(EstrategiaCosteo):
    """Implementa el costeo completo resultante integral (absorción de todos los costos)."""

    def calcular_costo_unitario(
        self,
        producto: Producto,
        capacidad: CapacidadInstalada,
        parametros: ParametrosCosteo
    ) -> float:
        # Lógica: (Costo Variable + CIF Variables + CIF Fijos Totales) / Producción Real
        costo_variable = producto.precio_bobina_kg * (producto.gramaje / 1000)
        
        # Asumimos que datos_financieros contiene la desagregación necesaria
        cif_variables = parametros.cif_variables_totales
        cif_fijos = parametros.cif_fijos_totales
        produccion_real = parametros.produccion_real
        
        total_costos = costo_variable + cif_variables + cif_fijos
        
        return total_costos / produccion_real if produccion_real > 0 else 0.0
