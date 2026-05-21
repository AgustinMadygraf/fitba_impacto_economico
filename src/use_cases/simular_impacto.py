"""
Path: src/use_cases/simular_impacto.py
"""

from typing import Optional, Any
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
        capacidad: CapacidadInstalada,
        logger: Any  # Inyectamos el logger como dependencia (Duck Typing o Interfaz)
    ):
        self.inversion = inversion
        self.producto = producto
        self.oee_base = oee_base
        self.produccion = produccion
        self.escenario = escenario
        self.capacidad = capacidad
        self.horizonte_maximo = 24
        self.logger = logger

    def ejecutar(self) -> Optional[int]:
        """
        Ejecuta la simulación y retorna el mes de repago.
        """
        beneficio_acumulado = 0.0
        disponibilidad_t = self.oee_base.disponibilidad
        inversion_objetivo = self.inversion.monto_actualizado
        
        self.logger.debug(f"Iniciando simulación: {self.escenario.nombre}")
        
        for mes in range(1, self.horizonte_maximo + 1):
            disponibilidad_t *= (1 + self.escenario.tasa_crecimiento)
            volumen_t = self._calcular_volumen_produccion(disponibilidad_t)
            beneficio_mensual = self._calcular_beneficio_mensual(volumen_t)
            
            if beneficio_mensual > 0:
                beneficio_acumulado += beneficio_mensual
            
            self.logger.debug(
                f"Mes {mes:02d} | Disp: {disponibilidad_t:,.4f} | Vol: {volumen_t:,.0f} | "
                f"Ben.Mensual: ${beneficio_mensual:,.2f} | Acum: ${beneficio_acumulado:,.2f}"
            )
            
            if beneficio_acumulado >= inversion_objetivo:
                return mes
            
        return None

    def _calcular_volumen_produccion(self, disponibilidad_t: float) -> float:
        disponibilidad_activa = min(disponibilidad_t, self.capacidad.limite_disponibilidad)
        
        if disponibilidad_t > self.capacidad.limite_disponibilidad:
            self.logger.warning(f"Saturación de capacidad: {disponibilidad_t:,.4f} limitada a {self.capacidad.limite_disponibilidad}")

        produccion_potencial = self.produccion.volumen_base * (disponibilidad_activa / self.oee_base.disponibilidad)
        return produccion_potencial * self.escenario.factor_demanda

    def _calcular_beneficio_mensual(self, volumen_producido: float) -> float:
        delta_volumen = volumen_producido - self.produccion.volumen_base
        return delta_volumen * self.producto.margen_contribucion_unitario
