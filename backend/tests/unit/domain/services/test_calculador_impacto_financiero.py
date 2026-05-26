import pytest
from src.domain.services.calculador_impacto_financiero import CalculadorImpactoFinanciero
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada

def test_calcular_tasa_absorcion_cif():
    calculador = CalculadorImpactoFinanciero()
    capacidad = CapacidadInstalada(
        capacidad_nominal_por_hora=100.0,
        horas_por_turno=8,
        turnos_por_dia=1,
        dias_habiles_por_mes=22,
        dias_inhabiles_mensuales=1,
        capacidad_normal_mensual=5000.0
    )
    # 50000 / 5000 = 10.0
    tasa = calculador.calcular_tasa_absorcion_cif(capacidad, 50000.0)
    assert tasa == 10.0
    
    # Test zero capacity
    capacidad_zero = CapacidadInstalada(
        capacidad_nominal_por_hora=100.0,
        horas_por_turno=8,
        turnos_por_dia=1,
        dias_habiles_por_mes=22,
        dias_inhabiles_mensuales=1,
        capacidad_normal_mensual=0.0
    )
    assert calculador.calcular_tasa_absorcion_cif(capacidad_zero, 50000.0) == 0.0

