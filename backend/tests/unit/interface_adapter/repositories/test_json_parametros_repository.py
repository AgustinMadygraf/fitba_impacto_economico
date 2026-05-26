import pytest
from src.interface_adapter.repositories.json_parametros_repository import JsonParametrosRepository

def test_json_parametros_repository_coverage():
    data = {
        "inversion": {"objetivo_anr": 1000.0, "fecha_base": "2025-01-01"},
        "ipc_serie": {"datos": {}},
        "catalogo": {"productos": [], "lineas": []},
        "mix_objetivo": [],
        "oee_base": {"disponibilidad": 0.1, "rendimiento": 0.4, "calidad": 0.8},
        "capacidad_instalada": {
            "capacidad_nominal_por_hora": 100.0,
            "horas_por_turno": 8,
            "turnos_por_dia": 1,
            "dias_habiles_por_mes": 22,
            "dias_inhabiles_mensuales": 1
        },
        "gestion_costos": {
            "capacidad_normal_mensual": 450000.0,
            "costos_fijos_mensuales": 50000.0,
            "costo_mod_unitario": 15.0,
            "costo_cif_variable_unitario": 5.0
        },
        "escenarios": {}
    }
    repo = JsonParametrosRepository(data)
    
    # Test ipc_override fallback
    assert repo.get_ipc_override() is None
    
    # Test get_estructura_costos
    costos = repo.get_estructura_costos()
    assert costos.capacidad_normal_mensual == 450000.0
