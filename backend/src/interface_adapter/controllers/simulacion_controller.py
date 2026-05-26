"""
Path: backend/src/interface_adapter/controllers/simulacion_controller.py
"""

from src.application.simular_impacto_economico_caso_uso import CasoUsoSimularImpactoEconomico
from src.domain.entities.entorno.escenario import Escenario
from src.domain.services.servicio_datos_simulacion import ServicioDatosSimulacion

class SimulacionController:
    def __init__(self, gateway, presenter, logger):
        self.gateway = gateway
        self.presenter = presenter
        self.logger = logger
        self.servicio_datos = ServicioDatosSimulacion(gateway)

    def ejecutar_simulacion(self):
        inversion = self.gateway.get_inversion()
        mix = self.gateway.get_mix_produccion()
        escenarios_data = self.gateway.get_escenarios_raw()
        ipc_override = self.gateway.get_ipc_override()
        oee_base = self.servicio_datos.obtener_oee()
        
        resultados = []
        proyecciones = {}
        
        for clave, datos in escenarios_data.items():
            escenario = Escenario(
                nombre=datos["nombre"],
                tasa_disponibilidad=datos.get("tasa_disponibilidad", datos.get("tasa_crecimiento_mensual", 0.0)),
                tasa_rendimiento=datos.get("tasa_rendimiento", 0.0),
                tasa_calidad=datos.get("tasa_calidad", 0.0),
                factor_demanda=datos.get("factor_demanda", 1.0)
            )
    
            simulador = CasoUsoSimularImpactoEconomico(
                servicio_datos=self.servicio_datos,
                inversion=inversion,
                mix_objetivo=mix,
                escenario=escenario, 
                ipc_override=ipc_override,
                logger=self.logger
            )
    
            mes_repago, serie_proyeccion = simulador.ejecutar()
            resultados.append({
                "escenario": escenario.nombre, 
                "tasa": escenario.tasa_disponibilidad, 
                "mes_repago": mes_repago,
                "viable": mes_repago is not None
            })
            proyecciones[clave] = serie_proyeccion
    
        self.presenter.presentar_resultados(
            target_repago=inversion.monto_actualizado,
            oee_base=oee_base.disponibilidad,
            resultados=resultados,
            proyecciones=proyecciones
        )
