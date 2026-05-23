"""
Path: src/infrastructure/settings/logger.py
"""

import logging
import sys

class EndpointFilter(logging.Filter):
    """
    Filtro para omitir peticiones ruidosas del navegador (ej: Chrome DevTools)
    en los registros de acceso de Uvicorn.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        return "com.chrome.devtools.json" not in record.getMessage()

def setup_uvicorn_logging():
    """
    Configura los loggers de uvicorn para aplicar filtros de ruido.
    """
    for logger_name in ("uvicorn.access", "uvicorn.error"):
        logger = logging.getLogger(logger_name)
        if not any(isinstance(f, EndpointFilter) for f in logger.filters):
            logger.addFilter(EndpointFilter())

def get_logger(name: str = "FITBA", debug: bool = False):
    """
    Retorna un logger configurado con la apariencia de FastAPI/Uvicorn.
    Recibe un booleano 'debug' para determinar el nivel.
    """
    # Siempre ejecutamos el setup de uvicorn por seguridad al pedir un logger
    setup_uvicorn_logging()
    
    level = logging.DEBUG if debug else logging.INFO
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter('%(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    
    for handler in logger.handlers:
        handler.setLevel(level)
        
    return logger
