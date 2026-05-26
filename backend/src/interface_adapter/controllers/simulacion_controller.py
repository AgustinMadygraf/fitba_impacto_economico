"""
Path: backend/src/interface_adapter/controllers/simulacion_controller.py
"""

from src.application.simular_impacto_economico_caso_uso import CasoUsoSimularImpactoEconomico
from src.interface_adapter.repositories.json_parametros_repository import JsonParametrosRepository

class SimulacionController:
    def __init__(self, gateway, presenter, logger):
        self.gateway = gateway
        self.presenter = presenter
        self.logger = logger
        self.servicio_datos = None # Will be set later or via factory

    def set_servicio_datos(self, servicio_datos):
        self.servicio_datos = servicio_datos

    def ejecutar_simulacion(self):
        # Deprecated: use ejecutar_simulacion_con_payload
        self.ejecutar_simulacion_con_payload(self.gateway._data)

    def ejecutar_simulacion_con_payload(self, payload_dict):
        # Mover lógica de preparación de repositorio aquí
        self.gateway = JsonParametrosRepository(payload_dict)
        
        inversion = self.gateway.get_inversion()
        mix = self.gateway.get_mix_produccion()
        escenarios_data = self.gateway.get_escenarios_raw()
        ipc_override = self.gateway.get_ipc_override()
        # servicio_datos needs to be initialized with gateway
        from src.domain.services.servicio_datos_simulacion import ServicioDatosSimulacion
        self.servicio_datos = ServicioDatosSimulacion(self.gateway)
        oee_base = self.servicio_datos.obtener_oee()
    
        resultados = []
        proyecciones = {}
        mes_repago = None
        
        for clave, datos in escenarios_data.items():
            from src.domain.entities.entorno.escenario import Escenario
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
            self.logger.info(f"Proyeccion agregada para {escenario.nombre}: {len(serie_proyeccion)} puntos")
            proyecciones[escenario.nombre] = serie_proyeccion
            resultados.append({
                "escenario": escenario.nombre,
                "tasa": escenario.tasa_disponibilidad,
                "mes_repago": mes_repago,
                "viable": mes_repago is not None
            })
            
        self.presenter.presentar_resultados(mes_repago, oee_base.valor, resultados, proyecciones)
