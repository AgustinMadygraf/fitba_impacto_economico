"""
Path: backend/src/domain/services/calculador_ingresos.py
"""

from typing import Dict, List, Tuple
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.comercial.produccion import MixProduccion

class CalculadorIngresos:
    @staticmethod
    def calcular_beneficio_mensual(
        productos: Dict[str, Producto], 
        mix: MixProduccion, 
        vol_prod: float, 
        vol_ventas: float
    ) -> Tuple[float, float, float]:
        ingresos_totales = 0.0
        costos_totales = 0.0
        
        for prod_id, porcentaje in mix.porcentajes.items():
            producto = productos.get(prod_id)
            if not producto: continue
            
            # Asumimos que el mix se aplica tanto a la producción como a las ventas
            ingresos_totales += (vol_ventas * porcentaje) * producto.precio_unitario
            costos_totales += (vol_prod * porcentaje) * producto.costo_marginal_unitario
            
        beneficio_total = ingresos_totales - costos_totales
        return beneficio_total, ingresos_totales, costos_totales
