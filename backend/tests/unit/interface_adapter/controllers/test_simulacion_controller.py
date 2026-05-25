from unittest.mock import MagicMock
from src.interface_adapter.controllers.simulacion_controller import SimulacionController
from src.entities.financiero.inversion import Inversion
from src.entities.financiero.indice_financiero import IndiceFinanciero

def test_ejecutar_simulacion():
    gateway = MagicMock()
    presenter = MagicMock()
    logger = MagicMock()

    indice = IndiceFinanciero("IPC", {1: 0.1}, 0.1)
    inversion = Inversion(monto_anr=1000.0, fecha_base="2025-01-01", indice_base=indice)

    # Corregimos el mock del producto para que tenga los atributos necesarios
    mock_producto = MagicMock()
    mock_producto.id = "p1"
    mock_producto.precio_unitario = 10.0
    mock_producto.costo_marginal_unitario = 5.0

    gateway.get_inversion.return_value = inversion
    gateway.get_productos.return_value = [mock_producto]
    gateway.get_oee_base.return_value = MagicMock(valor=0.04, disponibilidad=0.1, rendimiento=0.44, calidad=0.84)
    gateway.get_lineas_produccion.return_value = [MagicMock(capacidad_nominal=1000.0)]
    gateway.get_capacidad_instalada.return_value = MagicMock(capacidad_nominal_total=1000.0)
    gateway.get_mix_produccion.return_value = MagicMock(porcentajes={"p1": 1.0})
    gateway.get_escenarios_raw.return_value = {"test": {"nombre": "test", "tasa_crecimiento_mensual": 0.01}}
    gateway.get_ipc_override.return_value = None

    controller = SimulacionController(gateway, presenter, logger)
    controller.ejecutar_simulacion()
    
    # Assert
    assert presenter.presentar_resultados.called
