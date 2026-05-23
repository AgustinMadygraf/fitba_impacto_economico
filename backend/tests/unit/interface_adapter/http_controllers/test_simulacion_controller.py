from unittest.mock import MagicMock
from src.interface_adapter.http_controllers.simulacion_controller import SimulacionController

def test_ejecutar_simulacion():
    # Setup mocks
    gateway = MagicMock()
    presenter = MagicMock()
    logger = MagicMock()
    
    # Prepara el gateway para retornar entidades con valores correctos
    gateway.get_inversion.return_value = MagicMock(monto_actualizado=1000.0)
    gateway.get_producto.return_value = MagicMock(margen_contribucion_unitario=5.0)
    gateway.get_oee_base.return_value = MagicMock(valor=0.04, disponibilidad=0.1)
    gateway.get_produccion_base.return_value = MagicMock(volumen_base=100.0)
    gateway.get_escenarios_raw.return_value = {
        "test": {"nombre": "test", "tasa_crecimiento_mensual": 0.01}
    }
    gateway.get_capacidad_instalada.return_value = MagicMock(limite_disponibilidad=0.5)
    
    controller = SimulacionController(gateway, presenter, logger)
    
    # Execute
    controller.ejecutar_simulacion()
    
    # Assert
    presenter.presentar_resultados.assert_called()
