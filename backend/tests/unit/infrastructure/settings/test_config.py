import pytest
import os
import json
from src.infrastructure.settings.config import ConfigLoader

@pytest.fixture
def mock_params(tmp_path):
    data = {
        "inversion": {"objetivo_anr": 1000.0, "factor_ipc_acumulado": 1.1},
        "oee": {"linea_base": {"disponibilidad": 0.5, "rendimiento": 0.6, "calidad": 0.7}, "limite_disponibilidad": 0.8},
        "productos": [{"id": "p1", "nombre": "Prod 1", "precio_unitario": 10.0, "costo_marginal_unitario": 5.0}],
        "lineas_produccion": [{"id": "l1", "nombre": "Linea 1", "capacidad_nominal": 100, "productos_compatibles": ["p1"]}],
        "mix_objetivo": [{"producto_id": "p1", "porcentaje": 1.0}],
        "escenarios": {"esc1": {"nombre": "E1", "tasa_crecimiento_mensual": 0.1, "factor_demanda": 1.0}}
    }
    d = tmp_path / "data"
    d.mkdir()
    f = d / "params.json"
    f.write_text(json.dumps(data))
    return str(f)

def test_config_loader_initialization(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    assert loader.config_path == mock_params
    assert loader._raw_data["inversion"]["objetivo_anr"] == 1000.0

def test_get_app_mode_default():
    if "APP_MODE" in os.environ:
        del os.environ["APP_MODE"]
    loader = ConfigLoader(config_path="data/params.json")
    assert loader.get_app_mode() == "development"

def test_get_app_mode_production():
    os.environ["APP_MODE"] = "production"
    loader = ConfigLoader(config_path="data/params.json")
    assert loader.get_app_mode() == "production"

def test_get_inversion(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    inversion = loader.get_inversion()
    assert inversion.monto_anr == 1000.0
    assert inversion.factor_ipc == 1.1

def test_get_productos(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    productos = loader.get_productos()
    assert len(productos) == 1
    assert productos[0].id == "p1"

def test_get_oee_base(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    oee = loader.get_oee_base()
    assert oee.disponibilidad == 0.5
    assert oee.rendimiento == 0.6
    assert oee.calidad == 0.7

def test_get_lineas_produccion(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    lineas = loader.get_lineas_produccion()
    assert len(lineas) == 1
    assert lineas[0].id == "l1"

def test_get_mix_produccion(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    mix = loader.get_mix_produccion()
    assert mix.porcentajes["p1"] == 1.0

def test_get_capacidad_instalada(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    capacidad = loader.get_capacidad_instalada()
    assert capacidad.limite_disponibilidad == 0.8

def test_get_start_time(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    start_time = loader.get_start_time()
    assert isinstance(start_time, str)
    # Debe ser una cadena ISO
    assert "T" in start_time

def test_is_debug_enabled_false(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    assert loader.is_debug_enabled() is False

def test_get_escenarios_raw(mock_params):
    loader = ConfigLoader(config_path=mock_params)
    escenarios = loader.get_escenarios_raw()
    assert "esc1" in escenarios
    assert escenarios["esc1"]["nombre"] == "E1"
