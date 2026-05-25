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
from src.application.ipc_calculator import IPCCalculator

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
            
            # Inflación using IPCCalculator
            factor_inflacion = 1.0
            if indice_base:
                # We need to simulate the "today" as the fecha_actual
                factor_inflacion = IPCCalculator.calculate_factor(indice_base, self.inversion.fecha_base, fecha_actual)
                target_actualizado_t = self.inversion.monto_anr * factor_inflacion
            else:
                target_actualizado_t = self.inversion.monto_anr
            
            disponibilidad_t *= (1 + self.escenario.tasa_crecimiento)
            
            # OEE
            oee_t = disponibilidad_t * self.oee_base.rendimiento * self.oee_base.calidad
            
            # Producción vs Ventas
            volumen_produccion_mensuales = self.capacidad_instalada.capacidad_nominal_total * min(oee_t, 1.0)
            volumen_ventas_mensuales = volumen_produccion_mensuales * self.escenario.factor_demanda
            
            beneficio_mensual, ingresos_mensuales, costos_mensuales = self._calcular_beneficio_mensual(
                volumen_produccion_mensuales, volumen_ventas_mensuales
            )
            
            # Acumular beneficio total
            beneficio_acumulado += beneficio_mensual
            
            # Calcular Valor Presente (deflactado por inflación acumulada)
            beneficio_acumulado_presente = beneficio_acumulado / factor_inflacion
            
            # Enriquecer resultado
            proyeccion_mensual.append({
                "mes": mes,
                "fecha": label_fecha,
                "volumen_produccion": volumen_produccion_mensuales,
                "volumen_ventas": volumen_ventas_mensuales,
                "ingresos_mensuales": ingresos_mensuales,
                "costos_mensuales": costos_mensuales,
                "beneficio_mensual": beneficio_mensual,
                "beneficio_acumulado": beneficio_acumulado,
                "beneficio_acumulado_presente": beneficio_acumulado_presente
            })
            
            if mes_repago is None and beneficio_acumulado >= target_actualizado_t:
                mes_repago = mes
            
        return mes_repago, proyeccion_mensual

    def _calcular_beneficio_mensual(self, vol_prod: float, vol_ventas: float) -> Tuple[float, float, float]:
        ingresos_totales = 0.0
        costos_totales = 0.0
        
        for prod_id, porcentaje in self.mix.porcentajes.items():
            producto = self.productos.get(prod_id)
            if not producto: continue
            
            # Asumimos que el mix se aplica tanto a la producción como a las ventas
            ingresos_totales += (vol_ventas * porcentaje) * producto.precio_unitario
            costos_totales += (vol_prod * porcentaje) * producto.costo_marginal_unitario
            
        beneficio_total = ingresos_totales - costos_totales
        return beneficio_total, ingresos_totales, costos_totales
