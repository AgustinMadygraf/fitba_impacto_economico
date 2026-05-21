"""
Punto de entrada principal para la simulación de impacto económico FITBA.
Bootstrap de la aplicación siguiendo Clean Architecture.
"""

from src.infrastructure.settings.config import ConfigLoader
from src.infrastructure.settings.logger import get_logger
from src.infrastructure.cli.rich import RichSimulacionPresenter
from src.interface_adapter.controller.simulacion_controller import SimulacionController

# Logger para eventos de sistema
logger = get_logger()

def run():
    # 1. Capa de Infraestructura (Implementaciones físicas)
    config_loader = ConfigLoader()
    rich_presenter = RichSimulacionPresenter()
    
    # 2. Capa de Interface Adapters (Orquestación)
    # Inyectamos el cargador como Gateway y el reportero como Presenter
    controller = SimulacionController(gateway=config_loader, presenter=rich_presenter)
    
    # 3. Ejecución
    logger.info("Sistema FITBA: Iniciando controlador de simulación...")
    controller.ejecutar_simulacion()
    logger.info("Sistema FITBA: Ejecución finalizada.")

if __name__ == "__main__":
    run()
