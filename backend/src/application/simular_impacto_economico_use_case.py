from datetime import datetime
from src.application.date_helper import add_months
from typing import Optional, Any, List, Dict, Tuple


from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import MixProduccion
from src.entities.escenario import Escenario
from src.entities.linea_produccion import LineaProduccion
from src.entities.capacidad_instalada import CapacidadInstalada

class SimularImpactoEconomico:
    
    def __init__(
        self, 
        inversion: Inversion, 
        productos: List[Producto],
        lineas_produccion: List[LineaProduccion],
        capacidad_instalada: CapacidadInstalada,
        mix_objetivo: MixProduccion,
        oee_base: OEE, 
        escenario: Escenario,
        logger: Any
    ):
        self.inversion = inversion
        self.productos = {p.id: p for p in productos}
        self.lineas = lineas_produccion
        self.capacidad_instalada = capacidad_instalada
        self.mix = mix_objetivo
        self.oee_base = oee_base
        self.escenario = escenario
        self.horizonte_maximo = 24
        self.logger = logger

    def ejecutar(self) -> Tuple[Optional[int], List[Dict[str, Any]]]:
        beneficio_acumulado = 0.0
        disponibilidad_t = self.oee_base.disponibilidad
        
        mes_repago = None
        proyeccion_mensual = []
        
        fecha_base = datetime.strptime(self.inversion.fecha_base, "%Y-%m-%d")
        
        beneficio_base = self._calcular_beneficio_mensual(self.capacidad_instalada.capacidad_nominal_total * self.oee_base.valor)
        
        for mes in range(1, self.horizonte_maximo + 1):
            fecha_actual = add_months(fecha_base, mes)
            label_fecha = fecha_actual.strftime("%m/%Y")
            
            # Inflación
            if self.inversion.indice_base:
                factor_inflacion = self.inversion.indice_base.calcular_factor_capitalizacion(mes)
                target_actualizado_t = self.inversion.monto_anr * factor_inflacion
            else:
                target_actualizado_t = self.inversion.monto_anr
            
            disponibilidad_t *= (1 + self.escenario.tasa_crecimiento)
            
            # OEE
            oee_t = disponibilidad_t * self.oee_base.rendimiento * self.oee_base.calidad
            capacidad_efectiva = self.capacidad_instalada.capacidad_nominal_total * min(oee_t, 1.0) * self.escenario.factor_demanda
            
            beneficio_mensual = self._calcular_beneficio_mensual(capacidad_efectiva)
            delta_beneficio = beneficio_mensual - beneficio_base
            
            if delta_beneficio > 0:
                beneficio_acumulado += delta_beneficio
            
            # Enriquecer resultado con etiqueta temporal
            proyeccion_mensual.append({
                "mes": mes,
                "fecha": label_fecha,
                "beneficio_acumulado": beneficio_acumulado
            })
            
            if mes_repago is None and beneficio_acumulado >= target_actualizado_t:
                mes_repago = mes
            
        return mes_repago, proyeccion_mensual

    def _calcular_beneficio_mensual(self, volumen_total: float) -> float:
        beneficio_total = 0.0
        for prod_id, porcentaje in self.mix.porcentajes.items():
            producto = self.productos.get(prod_id)
            if not producto: continue
            
            beneficio_total += (volumen_total * porcentaje) * producto.margen_contribucion_unitario
            
        return beneficio_total
