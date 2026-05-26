"""
Path: backend/src/domain/services/costeo/completo_resultante_absorcion.py
"""

from typing import Dict
from src.domain.services.costeo.estrategia_costeo import EstrategiaCosteo
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada

class CompletoResultanteAbsorcion(EstrategiaCosteo):
    """Implementa el costeo completo resultante por absorción."""

    def calcular_costo_unitario(
        self,
        producto: Producto,
        capacidad: CapacidadInstalada,
        datos_financieros: Dict
    ) -> float:
        # Lógica: Costo Variable Unitario + (Costos Fijos Totales / Producción Real)
        # Nota: En esta estrategia, los costos fijos se absorben según la producción real
        
        costo_variable = producto.precio_bobina_kg * (producto.gramaje / 1000) # Simplificación
        
        costos_fijos_totales = datos_financieros.get("costos_fijos_totales", 0.0)
        produccion_real = datos_financieros.get("produccion_real", 1.0)
        
        absorcion_fijos = costos_fijos_totales / produccion_real if produccion_real > 0 else 0.0
        
        return costo_variable + absorcion_fijos
