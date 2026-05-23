"""
Path: main.py
"""

from src.infrastructure.settings.config import ConfigLoader
from src.infrastructure.settings.logger import get_logger
from src.infrastructure.cli.rich import RichSimulacionPresenter
from src.interface_adapter.controller.simulacion_controller import SimulacionController

def run():
    # 1. Carga de configuración (incluye detección de --debug)
    config = ConfigLoader()
    is_debug = config.is_debug_enabled()
    
    # 2. Inicialización de Loggers (Sin importar la librería logging)
    main_logger = get_logger("FITBA.Main")
    sim_logger = get_logger("FITBA.Simulacion")
    
    # 3. Ensamblaje y Ejecución
    controller = SimulacionController(
        gateway=config, 
        presenter=RichSimulacionPresenter(), 
        logger=sim_logger
    )
    
    main_logger.info("Sistema FITBA: Iniciando controlador de simulación...")
    controller.ejecutar_simulacion()
    main_logger.info("Sistema FITBA: Ejecución finalizada.")

if __name__ == "__main__":
    run()
