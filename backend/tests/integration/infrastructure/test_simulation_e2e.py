import pytest
from fastapi.testclient import TestClient
from src.infrastructure.api_gateway.app import app

client = TestClient(app)

def test_full_simulation_flow():
    # Payload que representa el flujo completo que haría el frontend
    payload = {
        "inversion": {
            "objetivo_anr": 850000.0,
            "factor_ipc_acumulado": 1.0
        },
        "oee": {
            "disponibilidad": 0.135,
            "rendimiento": 0.44,
            "calidad": 0.84
        },
        "productos": [
            {
                "id": "p1",
                "nombre": "Bolsa Lisa",
                "precio_unitario": 150.0,
                "costo_marginal_unitario": 85.5
            }
        ],
        "lineas_produccion": [
            {
                "id": "l1",
                "nombre": "Linea 1",
                "capacidad_nominal": 450000.0,
                "productos_compatibles": ["p1"]
            }
        ],
        "mix_objetivo": [
            {
                "producto_id": "p1",
                "porcentaje": 1.0
            }
        ],
        "escenarios": {
            "test": {
                "nombre": "Test E2E",
                "tasa_crecimiento_mensual": 0.02,
                "factor_demanda": 1.0
            }
        }
    }

    # 1. Ejecutar simulación
    response = client.post("/api/v1/simulacion/ejecutar", json=payload)
    
    # 2. Verificar éxito
    assert response.status_code == 200
    data = response.json()
    
    assert data["exito"] is True
    assert "resultados" in data
    assert "proyecciones" in data
    assert "test" in data["proyecciones"]
    assert len(data["proyecciones"]["test"]) == 24
