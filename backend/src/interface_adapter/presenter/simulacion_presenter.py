from abc import ABC, abstractmethod

class SimulacionPresenter(ABC):
    """
    Interfaz de Presentación. 
    Define cómo deben entregarse los resultados de la simulación.
    """
    
    @abstractmethod
    def presentar_resultados(
        self, 
        target_repago: float, 
        oee_base: float, 
        resultados: list,
        proyecciones: dict = None
    ):
        """
        Contrato para la visualización del informe de impacto económico.
        """
        pass
