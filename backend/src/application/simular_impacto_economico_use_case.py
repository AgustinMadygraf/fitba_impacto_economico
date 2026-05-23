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
from src.entities.indice_financiero import IndiceFinanciero

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
        logger: Any,
        ipc_override: Optional[float] = None
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
        self.ipc_override = ipc_override

    def ejecutar(self) -> Tuple[Optional[int], List[Dict[str, Any]]]:
        beneficio_acumulado = 0.0
        disponibilidad_t = self.oee_base.disponibilidad
        
        mes_repago = None
        proyeccion_mensual = []
        
        fecha_base = datetime.strptime(self.inversion.fecha_base, "%Y-%m-%d")
        
        # Override IPC if provided
        indice_base = self.inversion.indice_base
        if self.ipc_override is not None and indice_base:
            # Create a new IndiceFinanciero with the overridden rate
            indice_base = IndiceFinanciero(
                nombre=indice_base.nombre,
                serie_mensual=indice_base.serie_mensual,
                tasa_proyectada=self.ipc_override
            )
        
        for mes in range(1, self.horizonte_maximo + 1):
            fecha_actual = add_months(fecha_base, mes)
            label_fecha = fecha_actual.strftime("%m/%Y")
            
            # Inflación
            factor_inflacion = 1.0
            if indice_base:
                factor_inflacion = indice_base.calcular_factor_capitalizacion(mes)
                target_actualizado_t = self.inversion.monto_anr * factor_inflacion
            else:
                target_actualizado_t = self.inversion.monto_anr
            
            disponibilidad_t *= (1 + self.escenario.tasa_crecimiento)
            
            # OEE
            oee_t = disponibilidad_t * self.oee_base.rendimiento * self.oee_base.calidad
            capacidad_efectiva = self.capacidad_instalada.capacidad_nominal_total * min(oee_t, 1.0) * self.escenario.factor_demanda
            
            beneficio_mensual = self._calcular_beneficio_mensual(capacidad_efectiva)
            
            # Acumular beneficio total
            beneficio_acumulado += beneficio_mensual
            
            # Calcular Valor Presente (deflactado por inflación acumulada)
            beneficio_acumulado_presente = beneficio_acumulado / factor_inflacion
            
            # Enriquecer resultado
            proyeccion_mensual.append({
                "mes": mes,
                "fecha": label_fecha,
                "beneficio_acumulado": beneficio_acumulado,
                "beneficio_acumulado_presente": beneficio_acumulado_presente
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
