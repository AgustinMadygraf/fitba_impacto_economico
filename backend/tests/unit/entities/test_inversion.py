from src.entities.inversion import Inversion
from src.entities.indice_financiero import IndiceFinanciero
import pytest

def test_inversion_monto_actualizado():
    inversion = Inversion(monto_anr=1000.0, factor_correccion_inicial=1.5)
    assert inversion.monto_actualizado == 1500.0

def test_inversion_target_proyectado():
    indice = IndiceFinanciero(nombre="IPC", serie_mensual={1: 0.1}, tasa_proyectada=0.1)
    inversion = Inversion(monto_anr=1000.0, indice_base=indice, factor_correccion_inicial=1.0)
    
    # Mes 1: 1000 * 1.1 = 1100
    assert inversion.calcular_target_proyectado(1) == pytest.approx(1100.0)
    # Mes 2: 1000 * (1.1 * 1.1) = 1210
    assert inversion.calcular_target_proyectado(2) == pytest.approx(1210.0)
