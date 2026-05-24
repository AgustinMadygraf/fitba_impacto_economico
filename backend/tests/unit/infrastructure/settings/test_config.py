import pytest
from src.infrastructure.settings.config import ConfigLoader

def test_load_config_valid(tmp_path):
    # Mocking the JSON content
    data = {
        "inversion": {"objetivo_anr": 1000.0, "fecha_base": "2025-01-01"},
        "capacidad_instalada": {"capacidad_nominal_total_mensual": 100.0},
        "oee_base": {"disponibilidad": 0.5, "rendimiento": 0.6, "calidad": 0.7},
        "catalogo": {
            "productos": [{"id": "p1", "nombre": "Prod1", "precio": 10.0, "costo": 5.0}],
            "lineas": [{"id": "l1", "nombre": "Lin1", "capacidad_nominal": 100.0, "productos_compatibles": ["p1"]}]
        },
        "mix_objetivo": [{"producto_id": "p1", "porcentaje": 1.0}],
        "escenarios": {}
    }
    
    config_file = tmp_path / "params.json"
    with open(config_file, "w") as f:
        import json
        json.dump(data, f)
        
    loader = ConfigLoader(config_path=str(config_file))
    oee = loader.get_oee_base()
    
    assert oee.disponibilidad == 0.5
    assert oee.rendimiento == 0.6
    assert oee.calidad == 0.7
    # Ensure no limite_disponibilidad field
    assert not hasattr(oee, "limite_disponibilidad")
