"""
Path: src/entities/escenario.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Escenario:
    """
    Representa los parámetros variables de un escenario de simulación.
    
    Atributos:
        nombre (str): Identificador del escenario (ej: "Proyectado").
        tasa_crecimiento (float): Crecimiento mensual compuesto de la disponibilidad OEE.
        factor_demanda (float): Tasa de absorción de la producción potencial. 
            Un valor de 1.0 indica que el mercado absorbe el 100% de lo producido 
            gracias a la mejora de eficiencia.
    """
    nombre: str
    tasa_crecimiento: float
    factor_demanda: float
