from unittest.mock import MagicMock
from src.interface_adapter.controllers.simulacion_controller import SimulacionController

def test_ejecutar_simulacion():
    gateway = MagicMock()
    presenter = MagicMock()
    logger = MagicMock()
    
    gateway.get_inversion.return_value = MagicMock(monto_actualizado=1000.0, calcular_target_proyectado=MagicMock(return_value=1100.0))
    # Mockear margen de contribución como float explícito
    mock_producto = MagicMock()
    mock_producto.margen_contribucion_unitario = 5.0
    gateway.get_productos.return_value = [mock_producto]
    gateway.get_oee_base.return_value = MagicMock(valor=0.04, disponibilidad=0.1, rendimiento=0.44, calidad=0.84)
    gateway.get_lineas_produccion.return_value = [MagicMock(capacidad_nominal=1000.0)]
    gateway.get_capacidad_instalada.return_value = MagicMock(capacidad_nominal_total=1000.0)
    gateway.get_mix_produccion.return_value = MagicMock(porcentajes={"p1": 1.0})
    gateway.get_escenarios_raw.return_value = {"test": {"nombre": "test", "tasa_crecimiento_mensual": 0.01}}
    
    controller = SimulacionController(gateway, presenter, logger)
    controller.ejecutar_simulacion()
    presenter.presentar_resultados.assert_called()
