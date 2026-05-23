from src.entities.indice_financiero import IndiceFinanciero

def test_indice_financiero_acumulado_lineal():
    # 4% mensual fijo
    indice = IndiceFinanciero(nombre="Test", serie_mensual={1: 0.04, 2: 0.04}, tasa_proyectada=0.04)
    # Mes 1: 1.04
    # Mes 2: 1.04 * 1.04 = 1.0816
    assert round(indice.calcular_factor_capitalizacion(1), 4) == 1.0400
    assert round(indice.calcular_factor_capitalizacion(2), 4) == 1.0816

def test_indice_financiero_acumulado_proyectado():
    indice = IndiceFinanciero(nombre="Test", serie_mensual={1: 0.10}, tasa_proyectada=0.05)
    # Mes 1: 1.10
    # Mes 2: 1.10 * 1.05 = 1.155
    assert round(indice.calcular_factor_capitalizacion(2), 3) == 1.155
