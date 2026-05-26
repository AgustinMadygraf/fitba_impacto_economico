import pytest
import os
import json
from unittest.mock import patch
from src.infrastructure.settings.config import ConfigLoader

@pytest.fixture
def mock_params(tmp_path):
    data = {
        "inversion": {"objetivo_anr": 1000.0, "fecha_base": "2025-01-01"},
        "capacidad_instalada": {
            "capacidad_nominal_por_hora": 100.0,
            "horas_por_turno": 8,
            "turnos_por_dia": 1,
            "dias_habiles_por_mes": 22,
            "dias_inhabiles_mensuales": 1
        },
        "oee_base": {"disponibilidad": 0.5, "rendimiento": 0.6, "calidad": 0.7},
        "catalogo": {
            "productos": [{"id": "p1", "nombre": "Prod1", "precio": 10.0, "costo": 5.0}],
            "lineas": [{"id": "l1", "nombre": "Lin1", "capacidad_nominal": 100.0, "productos_compatibles": ["p1"]}]
        },
        "mix_objetivo": [{"producto_id": "p1", "porcentaje": 1.0}],
        "escenarios": {"test": {"nombre": "t", "tasa_crecimiento_mensual": 0.01, "factor_demanda": 1.0}}
    }
    config_file = tmp_path / "params.json"
    with open(config_file, "w") as f:
        json.dump(data, f)
    return str(config_file)

def test_load_config_valid(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    oee = loader.get_oee_base()
    
    assert oee.disponibilidad == 0.5
    assert oee.rendimiento == 0.6
    assert oee.calidad == 0.7

def test_cli_args_debug(mock_params):
    with patch("sys.argv", ["prog", "--debug"]):
        loader = ConfigLoader(config_path=mock_params)
        assert loader.is_debug_enabled() is True

def test_app_mode(mock_params):
    with patch.dict(os.environ, {"APP_MODE": "production"}):
        loader = ConfigLoader(config_path=mock_params)
        assert loader.get_app_mode() == "production"

def test_get_inversion_no_ipc(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    inversion = loader.get_inversion()
    assert inversion.indice_base is None

def test_get_escenarios_raw(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    escenarios = loader.get_escenarios_raw()
    assert "test" in escenarios

def test_get_ipc_override(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    assert loader.get_ipc_override() is None
