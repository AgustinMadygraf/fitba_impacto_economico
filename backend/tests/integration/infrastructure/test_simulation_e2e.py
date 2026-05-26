import pytest
from fastapi.testclient import TestClient
from src.infrastructure.web.routes import app

client = TestClient(app)

def test_full_simulation_flow():
    payload = {
        "inversion": {"objetivo_anr": 850000.0, "fecha_base": "2025-02-01"},
        "oee_base": {
            "disponibilidad": 0.135,
            "rendimiento": 0.44,
            "calidad": 0.84
        },
        "catalogo": {
            "productos": [
                {
                    "sku": "p1",
                    "nombre": "Bolsa Lisa",
                    "precio_unitario": 150.0,
                    "costo_marginal_unitario": 85.5
                }
            ],
            "lineas": [
                {
                    "sku": "l1",
                    "nombre": "Linea 1",
                    "capacidad_nominal": 450000.0,
                    "productos_compatibles": ["p1"]
                }
            ]
        },
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
        },
        "capacidad_instalada": {
            "capacidad_nominal_por_hora": 2500.0,
            "horas_por_turno": 8,
            "turnos_por_dia": 1,
            "dias_habiles_por_mes": 22,
            "dias_inhabiles_mensuales": 1
        }
    }

    response = client.post("/api/v1/simulacion/ejecutar", json=payload)
    assert response.status_code == 200
