import pytest
from src.use_cases.simular_impacto_economico import SimularImpactoEconomico
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import MixProduccion
from src.entities.linea_produccion import LineaProduccion
from src.entities.escenario import Escenario
from unittest.mock import MagicMock

def test_simular_impacto_economico_repago():
    # Setup
    inversion = Inversion(monto_anr=1000.0, factor_correccion_inicial=1.1)
    
    productos = [
        Producto(id="p1", nombre="Producto 1", precio_unitario=10.0, costo_marginal_unitario=5.0)
    ]
    
    lineas = [
        # Capacidad alta para asegurar repago en el test
        LineaProduccion(id="l1", nombre="Linea 1", capacidad_nominal=10000.0, productos_compatibles=["p1"])
    ]
    
    mix = MixProduccion(porcentajes={"p1": 1.0})
    
    oee_base = OEE(disponibilidad=0.1, rendimiento=0.44, calidad=0.84)
    escenario = Escenario(nombre="Test", tasa_crecimiento=0.10, factor_demanda=1.0)
    
    logger = MagicMock()

    simulacion = SimularImpactoEconomico(
        inversion=inversion,
        productos=productos,
        lineas_produccion=lineas,
        mix_objetivo=mix,
        oee_base=oee_base,
        escenario=escenario,
        logger=logger
    )

    # Execute
    mes_repago, proyecciones = simulacion.ejecutar()

    # Assert
    assert mes_repago is not None
    assert isinstance(mes_repago, int)
    assert mes_repago <= 24
    assert len(proyecciones) == 24
    assert proyecciones[-1] >= 1100
