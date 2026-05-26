"""
Path: backend/src/domain/entities/entorno/escenario.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Escenario:
    """
    Representa los parámetros variables de un escenario de simulación.
    
    Atributos:
        nombre (str): Identificador del escenario (ej: "Proyectado").
        tasa_disponibilidad (float): Crecimiento mensual compuesto de la disponibilidad OEE.
        tasa_rendimiento (float): Crecimiento mensual compuesto del rendimiento OEE.
        tasa_calidad (float): Crecimiento mensual compuesto de la calidad OEE.
        factor_demanda (float): Tasa de absorción de la producción potencial. 
            Un valor de 1.0 indica que el mercado absorbe el 100% de lo producido 
            gracias a la mejora de eficiencia.
    """
    nombre: str
    tasa_disponibilidad: float
    tasa_rendimiento: float
    tasa_calidad: float
    factor_demanda: float
