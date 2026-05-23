import logging
import sys
import os

class EndpointFilter(logging.Filter):
    """
    Filtro para omitir peticiones ruidosas del navegador.
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

def get_logger(name: str = "FITBA"):
    """
    Retorna un logger configurado. El nivel se determina por la variable de entorno LOG_LEVEL.
    """
    setup_uvicorn_logging()
    
    # Obtener nivel de log, default WARNING para producción
    level_name = os.getenv("LOG_LEVEL", "WARNING").upper()
    level = getattr(logging, level_name, logging.WARNING)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False
    
    # Asegurar que los handlers existentes tengan el nivel correcto
    for handler in logger.handlers:
        handler.setLevel(level)
        
    return logger
