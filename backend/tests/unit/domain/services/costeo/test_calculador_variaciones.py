import pytest
from src.domain.services.costeo.calculador_variaciones import CalculadorVariaciones

def test_calculador_variaciones():
    calc = CalculadorVariaciones()
    
    # Capacidad
    assert calc.calcular_variacion_capacidad(100.0, 80.0, 10.0) == 200.0
    
    # Eficiencia
    assert calc.calcular_variacion_eficiencia(10.0, 8.0, 100.0) == 200.0
    
    # Volumen
    assert calc.calcular_variacion_volumen(100.0, 80.0, 5.0) == 100.0
