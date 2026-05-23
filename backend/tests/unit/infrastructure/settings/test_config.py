import pytest
import os
import json
from src.infrastructure.settings.config import ConfigLoader

@pytest.fixture
def mock_params(tmp_path):
    data = {
        "inversion": {"objetivo_anr": 1000.0},
        "ipc_serie": {"nombre": "IPC Test", "serie_mensual": {"1": 0.05}, "tasa_proyectada": 0.03},
        "oee_base": {"disponibilidad": 0.5, "rendimiento": 0.6, "calidad": 0.7, "limite_disponibilidad": 0.8},
        "catalogo": {
            "productos": [{"id": "p1", "nombre": "Prod 1", "precio": 10.0, "costo": 5.0}],
            "lineas": [{"id": "l1", "nombre": "Linea 1", "capacidad_nominal": 100, "productos_compatibles": ["p1"]}]
        },
        "mix_objetivo": [{"producto_id": "p1", "porcentaje": 1.0}],
        "escenarios": {"esc1": {"nombre": "E1", "tasa_crecimiento_mensual": 0.1, "factor_demanda": 1.0}},
        "capacidad_instalada": {"capacidad_nominal_total_mensual": 500.0}
    }
    d = tmp_path / "data"
    d.mkdir()
    f = d / "params.json"
    f.write_text(json.dumps(data))
    return str(f)

def test_get_capacidad_instalada(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    capacidad = loader.get_capacidad_instalada()
    assert capacidad.capacidad_nominal_total == 500.0
