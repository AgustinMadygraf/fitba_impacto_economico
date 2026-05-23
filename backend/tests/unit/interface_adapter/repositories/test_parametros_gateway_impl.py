from unittest.mock import MagicMock
from src.interface_adapter.repositories.json_parametros_repository import JsonParametrosRepository

def test_parametros_gateway_impl_mapping():
    raw_data = {
        "inversion": {"objetivo_anr": 1000.0, "fecha_base": "2025-01-01"},
        "catalogo": {
            "productos": [{"id": "p1", "nombre": "Prod1", "precio": 10.0, "costo": 5.0}],
            "lineas": [{"id": "l1", "nombre": "Lin1", "capacidad_nominal": 100.0, "productos_compatibles": ["p1"]}]
        },
        "mix_objetivo": [{"producto_id": "p1", "porcentaje": 1.0}],
        "oee_base": {
            "disponibilidad": 0.1, "rendimiento": 0.4, "calidad": 0.8, "limite_disponibilidad": 0.9
        },
        "escenarios": {"test": {"nombre": "Test", "tasa_crecimiento_mensual": 0.01}}
    }
    
    gateway = JsonParametrosRepository(raw_data)
    inversion = gateway.get_inversion()
    assert inversion.monto_anr == 1000.0
