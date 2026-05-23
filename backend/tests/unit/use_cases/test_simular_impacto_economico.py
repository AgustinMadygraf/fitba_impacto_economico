import pytest
from src.use_cases.simular_impacto_economico import SimularImpactoEconomico
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import MixProduccion
from src.entities.linea_produccion import LineaProduccion
from src.entities.escenario import Escenario
from src.entities.capacidad_instalada import CapacidadInstalada
from unittest.mock import MagicMock

def test_simular_impacto_repago():
    inversion = Inversion(monto_anr=1000.0)
    productos = [Producto(id="p1", nombre="P1", precio_unitario=10.0, costo_marginal_unitario=5.0)]
    lineas = [LineaProduccion(id="l1", nombre="L1", capacidad_nominal=10000.0, productos_compatibles=["p1"])]
    capacidad = CapacidadInstalada(capacidad_nominal_total=10000.0)
    mix = MixProduccion(porcentajes={"p1": 1.0})
    oee_base = OEE(disponibilidad=0.1, rendimiento=0.44, calidad=0.84)
    escenario = Escenario(nombre="Test", tasa_crecimiento=0.10, factor_demanda=1.0)
    
    simulacion = SimularImpactoEconomico(
        inversion=inversion, productos=productos, lineas_produccion=lineas,
        capacidad_instalada=capacidad, mix_objetivo=mix, oee_base=oee_base,
        escenario=escenario, logger=MagicMock()
    )

    mes_repago, proyecciones = simulacion.ejecutar()
    assert mes_repago is not None
    assert mes_repago <= 24
    assert proyecciones[-1] >= 1000.0
