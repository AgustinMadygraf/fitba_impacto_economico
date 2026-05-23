from typing import Optional, Any, List, Dict
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import MixProduccion
from src.entities.escenario import Escenario
from src.entities.linea_produccion import LineaProduccion

class SimularImpactoEconomico:
    """Caso de uso para calcular el punto de equilibrio en la inversión con modelo multiproducto."""
    
    def __init__(
        self, 
        inversion: Inversion, 
        productos: List[Producto],
        lineas_produccion: List[LineaProduccion],
        mix_objetivo: MixProduccion,
        oee_base: OEE, 
        escenario: Escenario,
        logger: Any
    ):
        self.inversion = inversion
        self.productos = {p.id: p for p in productos}
        self.lineas = lineas_produccion
        self.mix = mix_objetivo
        self.oee_base = oee_base
        self.escenario = escenario
        self.horizonte_maximo = 24
        self.logger = logger
        
        # Calcular capacidad total del sistema
        self.capacidad_total = sum(l.capacidad_nominal for l in lineas_produccion)

    def ejecutar(self) -> Optional[int]:
        beneficio_acumulado = 0.0
        disponibilidad_t = self.oee_base.disponibilidad
        inversion_objetivo = self.inversion.monto_actualizado
        
        for mes in range(1, self.horizonte_maximo + 1):
            disponibilidad_t *= (1 + self.escenario.tasa_crecimiento)
            
            # 1. Capacidad efectiva total
            capacidad_efectiva = self._calcular_capacidad_efectiva(disponibilidad_t)
            
            # 2. Beneficio ponderado por mix
            beneficio_mensual = self._calcular_beneficio_mensual(capacidad_efectiva)
            
            if beneficio_mensual > 0:
                beneficio_acumulado += beneficio_mensual
            
            if beneficio_acumulado >= inversion_objetivo:
                return mes
            
        return None

    def _calcular_capacidad_efectiva(self, disponibilidad_t: float) -> float:
        # TODO: Implementar lógica de cuello de botella por flujo de producción
        # Por ahora, usamos una simplificación agregada
        factor_disponibilidad = min(disponibilidad_t, 1.0) # Simplificación
        return self.capacidad_total * factor_disponibilidad * self.escenario.factor_demanda

    def _calcular_beneficio_mensual(self, volumen_total: float) -> float:
        beneficio_total = 0.0
        for prod_id, porcentaje in self.mix.porcentajes.items():
            producto = self.productos.get(prod_id)
            if not producto:
                continue
            
            volumen_producto = volumen_total * porcentaje
            beneficio_total += volumen_producto * producto.margen_contribucion_unitario
            
        return beneficio_total
