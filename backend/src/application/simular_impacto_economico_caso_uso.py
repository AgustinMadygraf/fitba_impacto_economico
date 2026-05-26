"""
Path: backend/src/application/simular_impacto_economico_caso_uso.py
"""

from datetime import datetime
from typing import Optional, Any, List, Dict, Tuple

from src.domain.entities.financiero.inversion import Inversion
from src.domain.entities.comercial.produccion import MixProduccion
from src.domain.entities.entorno.escenario import Escenario
from src.domain.services.calculador_impacto_operativo import CalculadorImpactoOperativo
from src.domain.services.calculador_impacto_financiero import CalculadorImpactoFinanciero
from src.domain.services.calculador_ingresos import CalculadorIngresos
from src.domain.services.servicio_datos_simulacion import ServicioDatosSimulacion
from src.domain.entities.financiero.indice_financiero import IndiceFinanciero
from src.infrastructure.utils.ayudante_fechas import agregar_meses

class CasoUsoSimularImpactoEconomico:
    
    def __init__(
        self,
        servicio_datos: ServicioDatosSimulacion,
        inversion: Inversion,
        mix_objetivo: MixProduccion,
        escenario: Escenario,
        logger: Any,
        ipc_override: Optional[float] = None
    ):
        self.servicio_datos = servicio_datos
        self.inversion = inversion
        self.mix = mix_objetivo
        self.escenario = escenario
        self.logger = logger
        self.ipc_override = ipc_override
        
        # Injecting domain services
        self.calculador_operativo = CalculadorImpactoOperativo()
        self.calculador_financiero = CalculadorImpactoFinanciero()
        self.calculador_ingresos = CalculadorIngresos()

    def ejecutar(self) -> Tuple[Optional[int], List[Dict[str, Any]]]:
        # Obtención de datos mediante el nuevo servicio
        productos = self.servicio_datos.obtener_productos_mapeados()
        oee_base = self.servicio_datos.obtener_oee()
        capacidad_instalada = self.servicio_datos.obtener_capacidad()
        
        beneficio_acumulado = 0.0
        oee_t = oee_base
        
        mes_repago = None
        proyeccion_mensual = []
        
        fecha_base = datetime.strptime(self.inversion.fecha_base, "%Y-%m-%d")
        
        indice_base = self.inversion.indice_base
        if self.ipc_override is not None and indice_base:
            indice_base = IndiceFinanciero(
                nombre=indice_base.nombre,
                serie_mensual=indice_base.serie_mensual,
                tasa_proyectada=self.ipc_override
            )
        
        for mes in range(1, 25): # Horizonte máximo 24
            fecha_actual = agregar_meses(fecha_base, mes)
            label_fecha = fecha_actual.strftime("%m/%Y")
            
            factor_inflacion, target_actualizado_t = self.calculador_financiero.calcular_inflacion(
                self.inversion, indice_base, fecha_actual
            )
            
            oee_t = oee_t.evolucionar(self.escenario)
            
            volumen_produccion_mensuales, volumen_ventas_mensuales = self.calculador_operativo.calcular_volumenes(
                oee_t.disponibilidad, oee_t, capacidad_instalada, self.escenario
            )
            
            beneficio_mensual, ingresos_mensuales, costos_mensuales = self.calculador_ingresos.calcular_beneficio_mensual(
                productos, self.mix, volumen_produccion_mensuales, volumen_ventas_mensuales
            )
            
            beneficio_acumulado += beneficio_mensual
            beneficio_acumulado_presente = beneficio_acumulado / factor_inflacion
            
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
