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
        
        # Iteración mensual (Cronograma de Planta)
        for mes in range(1, self.horizonte_maximo + 1):
            # 1. Evolución de la eficiencia
            disponibilidad_t *= (1 + self.escenario.tasa_crecimiento)
            
            # 2. Cálculo físico de la producción
            volumen_t = self._calcular_volumen_produccion(disponibilidad_t)
            
            # 3. Valoración económica
            beneficio_mensual = self._calcular_beneficio_mensual(volumen_t)
            
            if beneficio_mensual > 0:
                beneficio_acumulado += beneficio_mensual
            
            # 4. Verificación de Repago
            if beneficio_acumulado >= inversion_objetivo:
                return mes
            
        return None

    def _calcular_volumen_produccion(self, disponibilidad_t: float) -> float:
        """
        Resuelve el balance de producción física (Física de Planta).
        Aplica cuellos de botella operativos y límites de absorción del mercado.
        """
        # Límite físico de la planta
        disponibilidad_activa = min(disponibilidad_t, self.capacidad.limite_disponibilidad)
        
        # Transformación OEE -> Volumen: Pt = Volumen_Base * (Dt / D0)
        produccion_potencial = self.produccion.volumen_base * (disponibilidad_activa / self.oee_base.disponibilidad)
        
        # Restricción de Demanda (Factor de mercado)
        return min(produccion_potencial, self.produccion.volumen_base * self.escenario.factor_demanda)

    def _calcular_beneficio_mensual(self, volumen_producido: float) -> float:
        """
        Transforma volumen físico incremental en flujo de caja (Economía).
        Bt = (Pt - Volumen_Base) * Margen_Unitario
        """
        delta_volumen = volumen_producido - self.produccion.volumen_base
        return delta_volumen * self.producto.margen_contribucion_unitario
