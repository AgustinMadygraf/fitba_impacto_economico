from src.application.simular_impacto_economico_use_case import SimularImpactoEconomico
from src.entities.escenario import Escenario

class SimulacionController:
    def __init__(self, gateway, presenter, logger):
        self.gateway = gateway
        self.presenter = presenter
        self.logger = logger

    def ejecutar_simulacion(self):
        inversion = self.gateway.get_inversion()
        productos = self.gateway.get_productos()
        oee_base = self.gateway.get_oee_base()
        lineas = self.gateway.get_lineas_produccion()
        capacidad = self.gateway.get_capacidad_instalada()
        mix = self.gateway.get_mix_produccion()
    
        escenarios_data = self.gateway.get_escenarios_raw()
        ipc_override = self.gateway.get_ipc_override()
        
        resultados = []
        proyecciones = {}
        
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
                capacidad_instalada=capacidad,
                mix_objetivo=mix,
                oee_base=oee_base,
                escenario=escenario, ipc_override=ipc_override,
                logger=self.logger
            )
    
            mes_repago, serie_proyeccion = simulador.ejecutar()
            # Mapeo consistente para la UI
            resultados.append({
                "escenario": escenario.nombre, 
                "tasa": escenario.tasa_crecimiento, 
                "mes_repago": mes_repago,
                "viable": mes_repago is not None
            })
            proyecciones[clave] = serie_proyeccion
    
        self.presenter.presentar_resultados(
            target_repago=inversion.monto_actualizado,
            oee_base=oee_base.valor,
            resultados=resultados,
            proyecciones=proyecciones
        )
