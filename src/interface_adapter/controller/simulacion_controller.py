from typing import Any
from src.interface_adapter.gateway.parametros_gateway import ParametrosGateway
from src.interface_adapter.presenter.simulacion_presenter import SimulacionPresenter
from src.entities.escenario import Escenario
from src.use_cases.simular_impacto import SimularImpactoEconomico

class SimulacionController:
    """
    Orquestador de la ejecución de la simulación multiproducto.
    """
    
    def __init__(self, gateway: Any, presenter: SimulacionPresenter, logger: Any):
        self.gateway = gateway
        self.presenter = presenter
        self.logger = logger

    def ejecutar_simulacion(self):
        inversion = self.gateway.get_inversion()
        productos = self.gateway.get_productos()
        oee_base = self.gateway.get_oee_base()
        lineas = self.gateway.get_lineas_produccion()
        mix = self.gateway.get_mix_produccion()
        
        escenarios_data = self.gateway.get_escenarios_raw()
        resultados = []
        
        for clave, datos in escenarios_data.items():
            escenario = Escenario(
                nombre=datos["nombre"],
                tasa_crecimiento=datos["tasa_crecimiento_mensual"],
                factor_demanda=datos.get("factor_demanda", 1.0)
            )
            
            simulador = SimularImpactoEconomico(
                inversion=inversion,
                productos=productos,
                lineas_produccion=lineas,
                mix_objetivo=mix,
                oee_base=oee_base,
                escenario=escenario,
                logger=self.logger
            )
            
            mes_repago = simulador.ejecutar()
            
            resultados.append({
                "nombre": escenario.nombre,
                "tasa": escenario.tasa_crecimiento,
                "mes_repago": mes_repago
            })

        self.presenter.presentar_resultados(
            target_repago=inversion.monto_actualizado,
            oee_base=oee_base.valor,
            resultados=resultados
        )
