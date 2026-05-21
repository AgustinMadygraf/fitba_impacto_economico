"""
Path: src/infrastructure/settings/logger.py
"""

import logging
import sys

def get_logger(name: str = "FITBA", debug: bool = False):
    """
    Retorna un logger configurado con la apariencia de FastAPI/Uvicorn.
    Recibe un booleano 'debug' para determinar el nivel.
    """
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
