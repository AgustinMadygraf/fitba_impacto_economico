import pytest
from src.use_cases.simular_impacto import SimularImpactoEconomico
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import Produccion
from src.entities.escenario import Escenario
from src.entities.capacidad_instalada import CapacidadInstalada
from unittest.mock import MagicMock

def test_simular_impacto_repago():
    # Setup
    inversion = Inversion(monto_anr=1000.0, factor_ipc=1.1)  # 1100
    producto = Producto(nombre="Producto", precio_unitario=10.0, costos_marginales_unitarios=5.0) # margen 5
    oee_base = OEE(disponibilidad=0.1, rendimiento=0.44, calidad=0.84)
    produccion = Produccion(volumen_base=100.0, volumen_vector=[])
    escenario = Escenario(nombre="Test", tasa_crecimiento=0.01, factor_demanda=1.0)
    capacidad = CapacidadInstalada(limite_disponibilidad=0.5)
    logger = MagicMock()

    simulacion = SimularImpactoEconomico(
        inversion, producto, oee_base, produccion, escenario, capacidad, logger
    )

    # Execute
    mes_repago = simulacion.ejecutar()

    # Assert
    assert mes_repago is not None
    assert mes_repago <= 24
