from unittest.mock import MagicMock
from src.interface_adapter.http_controllers.simulacion_controller import SimulacionController

def test_ejecutar_simulacion():
    # Setup mocks
    gateway = MagicMock()
    presenter = MagicMock()
    logger = MagicMock()
    
    # Prepara el gateway para retornar entidades con valores correctos
    mock_inversion = MagicMock()
    mock_inversion.monto_actualizado = 1000.0
    mock_inversion.calcular_target_proyectado.return_value = 1100.0
    gateway.get_inversion.return_value = mock_inversion
    
    gateway.get_productos.return_value = [
        MagicMock(id="p1", margen_contribucion_unitario=5.0)
    ]
    # OEE con valores reales para evitar errores de multiplicación con MagicMock
    oee_base = MagicMock(valor=0.04, disponibilidad=0.1, rendimiento=0.44, calidad=0.84)
    gateway.get_oee_base.return_value = oee_base
    
    gateway.get_lineas_produccion.return_value = [
        MagicMock(id="l1", capacidad_nominal=1000.0)
    ]
    gateway.get_mix_produccion.return_value = MagicMock(porcentajes={"p1": 1.0})
    
    gateway.get_escenarios_raw.return_value = {
        "test": {"nombre": "test", "tasa_crecimiento_mensual": 0.01}
    }
    
    controller = SimulacionController(gateway, presenter, logger)
    
    # Execute
    controller.ejecutar_simulacion()
    
    # Assert
    presenter.presentar_resultados.assert_called()
