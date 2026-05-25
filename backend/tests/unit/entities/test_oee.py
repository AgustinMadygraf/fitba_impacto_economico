from src.domain.entities.operacional.oee import OEE
import pytest

def test_oee_calculation():
    oee = OEE(disponibilidad=0.1, rendimiento=0.5, calidad=0.8)
    assert oee.valor == pytest.approx(0.04)
