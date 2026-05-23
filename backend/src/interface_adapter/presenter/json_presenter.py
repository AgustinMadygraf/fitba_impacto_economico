from typing import List, Dict, Any

class JSONSimulacionPresenter:
    def __init__(self):
        self.response_data = {}

    def presentar_resultados(self, target_repago: float, oee_base: float, resultados: List[Dict[str, Any]], proyecciones: Dict[str, List[Dict[str, Any]]]):
        self.response_data = {
            "target_repago": target_repago,
            "oee_base": oee_base,
            "resultados": resultados,
            "proyecciones": proyecciones
        }
