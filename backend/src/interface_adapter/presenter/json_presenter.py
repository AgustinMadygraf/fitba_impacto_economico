from src.interface_adapter.presenter.simulacion_presenter import SimulacionPresenter

class JSONSimulacionPresenter(SimulacionPresenter):
    """
    Implementación del Presenter que transforma el output de la simulación
    a una estructura diccionario de Python serializable a JSON.
    """
    
    def __init__(self):
        self.response_data = {}

    def presentar_resultados(
        self, 
        target_repago: float, 
        oee_base: float, 
        resultados: list,
        proyecciones: dict = None
    ):
        """
        Guarda los resultados formateados en un formato plano de diccionario.
        """
        self.response_data = {
            "exito": True,
            "target_repago": target_repago,
            "oee_base": oee_base,
            "resultados": [
                {
                    "escenario": res['nombre'],
                    "tasa": res['tasa'],
                    "mes_repago": res['mes_repago'],
                    "viable": res['mes_repago'] is not None and res['mes_repago'] <= 24
                }
                for res in resultados
            ],
            "proyecciones": proyecciones or {}
        }
