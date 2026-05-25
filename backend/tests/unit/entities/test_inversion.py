from src.domain.entities.financiero.inversion import Inversion
from src.domain.entities.financiero.indice_financiero import IndiceFinanciero
import pytest

def test_inversion_monto_actualizado():
    inversion = Inversion(monto_anr=1000.0, fecha_base="2025-01-01")
    assert inversion.monto_actualizado == 1000.0

def test_inversion_target_proyectado():
    indice = IndiceFinanciero(nombre="IPC", serie_mensual={1: 0.1}, tasa_proyectada=0.1)
    inversion = Inversion(monto_anr=1000.0, fecha_base="2025-01-01", indice_base=indice)
    
    # Mes 1: 1000 * 1.1 = 1100
    assert inversion.calcular_target_proyectado(1) == pytest.approx(1100.0)
    # Mes 2: 1000 * (1.1 * 1.1) = 1210
    assert inversion.calcular_target_proyectado(2) == pytest.approx(1210.0)
