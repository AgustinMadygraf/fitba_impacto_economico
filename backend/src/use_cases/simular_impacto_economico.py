from typing import Optional, Any, List, Dict, Tuple
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import MixProduccion
from src.entities.escenario import Escenario
from src.entities.linea_produccion import LineaProduccion

class SimularImpactoEconomico:
    """Caso de uso para calcular el punto de equilibrio en la inversión con modelo multiproducto e inflación dinámica."""
    
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
        self.capacidad_total = sum(l.capacidad_nominal for l in lineas_produccion)

    def ejecutar(self) -> Tuple[Optional[int], List[float]]:
        """
        Ejecuta la simulación considerando que el target de inversión se capitaliza 
        mensualmente según la serie de IPC cargada.
        """
        beneficio_acumulado = 0.0
        disponibilidad_t = self.oee_base.disponibilidad
        
        mes_repago = None
        proyeccion_mensual = []
        
        # Volumen base operativo (inalterado por la optimización)
        capacidad_base = self.capacidad_total * self.oee_base.valor
        beneficio_base = self._calcular_beneficio_mensual(capacidad_base)
        
        for mes in range(1, self.horizonte_maximo + 1):
            # 1. Capitalización del Target (Inflación Exponencial)
            target_actualizado_t = self.inversion.calcular_target_proyectado(mes)
            
            # 2. Optimización de OEE (Crecimiento de disponibilidad)
            disponibilidad_t *= (1 + self.escenario.tasa_crecimiento)
            
            # 3. Nueva Capacidad Real
            oee_t = disponibilidad_t * self.oee_base.rendimiento * self.oee_base.calidad
            capacidad_efectiva = self.capacidad_total * min(oee_t, 1.0) * self.escenario.factor_demanda
            
            beneficio_mensual = self._calcular_beneficio_mensual(capacidad_efectiva)
            
            # Impacto económico = Beneficio Incremental
            delta_beneficio = beneficio_mensual - beneficio_base
            
            if delta_beneficio > 0:
                beneficio_acumulado += delta_beneficio
            
            proyeccion_mensual.append(beneficio_acumulado)
            
            self.logger.debug(f"Mes {mes}: Target={target_actualizado_t:.2f}, Acumulado={beneficio_acumulado:.2f}")

            # Condición de Parada: El beneficio acumulado debe ganarle al Target Inflacionado
            if mes_repago is None and beneficio_acumulado >= target_actualizado_t:
                mes_repago = mes
            
        return mes_repago, proyeccion_mensual

    def _calcular_beneficio_mensual(self, volumen_total: float) -> float:
        beneficio_total = 0.0
        for prod_id, porcentaje in self.mix.porcentajes.items():
            producto = self.productos.get(prod_id)
            if not producto:
                continue
            
            volumen_producto = volumen_total * porcentaje
            beneficio_total += volumen_producto * producto.margen_contribucion_unitario
            
        return beneficio_total
