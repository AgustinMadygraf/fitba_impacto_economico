"""
Path: src/infrastructure/settings/logger.py
"""

import logging
import sys

def get_logger(name: str = "FITBA"):
    """
    Retorna un logger configurado con la apariencia de FastAPI/Uvicorn.
    Formato: LEVEL:    Mensaje
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        # Formateador estilo FastAPI (Nivel en mayúsculas con padding)
        formatter = logging.Formatter('%(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger
