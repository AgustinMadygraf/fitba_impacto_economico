"""
Path: src/use_cases/simular_impacto.py
"""

from typing import Optional
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import Produccion
from src.entities.escenario import Escenario
from src.entities.capacidad_instalada import CapacidadInstalada

class SimularImpactoEconomico:
    """Caso de uso para calcular el punto de equilibrio en la inversión."""
    
    def __init__(
        self, 
        inversion: Inversion, 
        producto: Producto, 
        oee_base: OEE, 
        produccion: Produccion, 
        escenario: Escenario,
        capacidad: CapacidadInstalada
    ):
        self.inversion = inversion
        self.producto = producto
        self.oee_base = oee_base
        self.produccion = produccion
        self.escenario = escenario
        self.capacidad = capacidad
        self.horizonte_maximo = 24

    def ejecutar(self) -> Optional[int]:
        """
        Ejecuta la simulación y retorna el mes de repago.
        Retorna None si no se alcanza en el horizonte definido.
        """
        beneficio_acumulado = 0.0
        disponibilidad_t = self.oee_base.disponibilidad
        inversion_objetivo = self.inversion.monto_actualizado
        
        # Iteración mensual
        for mes in range(1, self.horizonte_maximo + 1):
            # 1. Crecimiento (Dt = Dt-1 * (1 + r))
            disponibilidad_t *= (1 + self.escenario.tasa_crecimiento)
            
            # Aplicar límite físico de la planta
            disponibilidad_activa = min(disponibilidad_t, self.capacidad.limite_disponibilidad)
            
            # 2. Cálculo de Producción y Beneficio
            # Pt = Volumen_Base * (Dt / D0)
            produccion_t = self.produccion.volumen_base * (disponibilidad_activa / self.oee_base.disponibilidad)
            
            # Limitar producción por factor de demanda
            produccion_limitada = min(produccion_t, self.produccion.volumen_base * self.escenario.factor_demanda)
            
            # Beneficio Mensual = (Pt - Volumen_Base) * Margen
            beneficio_mensual = (produccion_limitada - self.produccion.volumen_base) * self.producto.margen_contribucion_unitario
            
            # Solo sumamos beneficios positivos
            if beneficio_mensual > 0:
                beneficio_acumulado += beneficio_mensual
            
            # 3. Verificación de Repago
            if beneficio_acumulado >= inversion_objetivo:
                return mes
            
        return None
