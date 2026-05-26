import pytest
from src.domain.services.costeo.estrategia_costeo import EstrategiaCosteo
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada
from src.domain.services.costeo.parametros_costeo import ParametrosCosteo

def test_estrategia_costeo_interface():
    class EstrategiaConcreta(EstrategiaCosteo):
        def calcular_costo_unitario(self, p, c, params):
            return 1.0

    estrategia = EstrategiaConcreta()
    assert estrategia.calcular_costo_unitario(None, None, None) == 1.0

def test_estrategia_costeo_abstract():
    with pytest.raises(TypeError):
        EstrategiaCosteo()
