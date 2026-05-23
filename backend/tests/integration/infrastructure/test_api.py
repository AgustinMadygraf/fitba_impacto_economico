from fastapi.testclient import TestClient
from src.infrastructure.web.app import app

client = TestClient(app)

def test_get_params_endpoint():
    # Asumimos que data/params.json existe y es válido
    response = client.get("/api/v1/simulacion/parametros")
    assert response.status_code == 200
    assert "inversion" in response.json() and "productos" in response.json()

def test_post_simular_endpoint_invalid():
    response = client.post("/api/v1/simulacion/ejecutar", json={"invalid": "data"})
    assert response.status_code == 422 # Error de validación Pydantic
