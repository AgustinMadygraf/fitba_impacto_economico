from typing import List, Dict, Any, Optional

class JSONSimulacionPresenter:
    def __init__(self):
        self.response_data = {}

    def presentar_resultados(self, mes_repago: Optional[int], proyecciones: List[Dict[str, Any]]):
        self.response_data = {
            "mes_repago": mes_repago,
            "proyecciones": proyecciones
        }
