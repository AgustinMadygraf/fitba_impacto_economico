"""
Path: src/interface_adapter/controller/simulacion_controller.py
"""

from src.interface_adapter.gateway.parametros_gateway import ParametrosGateway
from src.interface_adapter.presenter.simulacion_presenter import SimulacionPresenter
from src.entities.escenario import Escenario
from src.use_cases.simular_impacto import SimularImpactoEconomico

class SimulacionController:
    """
    Orquestador de la ejecución de la simulación.
    Utiliza el Presenter como una interfaz abstracta de salida.
    """
    
    def __init__(self, gateway: ParametrosGateway, presenter: SimulacionPresenter):
        self.gateway = gateway
        self.presenter = presenter

    def ejecutar_simulacion(self):
        """
        Punto de entrada lógico para la operación de simulación completa.
        """
        inversion = self.gateway.get_inversion()
        producto = self.gateway.get_producto()
        oee_base = self.gateway.get_oee_base()
        produccion = self.gateway.get_produccion_base()
        capacidad = self.gateway.get_capacidad_instalada()
        
        escenarios_data = self.gateway.get_escenarios_raw()
        resultados = []
        
        for clave, datos in escenarios_data.items():
            escenario = Escenario(
                nombre=datos['nombre'],
                tasa_crecimiento=datos['tasa_crecimiento_mensual'],
                factor_demanda=1.0 
            )
            
            simulador = SimularImpactoEconomico(
                inversion=inversion,
                producto=producto,
                oee_base=oee_base,
                produccion=produccion,
                escenario=escenario,
                capacidad=capacidad
            )
            
            mes_repago = simulador.ejecutar()
            
            resultados.append({
                'nombre': escenario.nombre,
                'tasa': escenario.tasa_crecimiento,
                'mes_repago': mes_repago
            })

        # Delegar directamente al Presenter (que ahora es la interfaz de salida)
        self.presenter.presentar_resultados(
            target_repago=inversion.monto_actualizado,
            oee_base=oee_base.valor,
            resultados=resultados
        )
