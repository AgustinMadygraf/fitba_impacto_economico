import pytest
from src.interface_adapter.repositories.parametros_gateway_impl import DinamicoParametrosGateway

def test_parametros_gateway_impl_mapping():
    raw_data = {
        "inversion": {"objetivo_anr": 1000.0, "factor_ipc_acumulado": 1.1},
        "productos": [{"id": "p1", "nombre": "Prod1", "precio_unitario": 10.0, "costo_marginal_unitario": 5.0}],
        "lineas_produccion": [{"id": "l1", "nombre": "Lin1", "capacidad_nominal": 100.0, "productos_compatibles": ["p1"]}],
        "mix_objetivo": [{"producto_id": "p1", "porcentaje": 1.0}],
        "oee": {
            "linea_base": {"disponibilidad": 0.1, "rendimiento": 0.4, "calidad": 0.8},
            "limite_disponibilidad": 0.9
        },
        "escenarios": {"test": {"nombre": "Test", "tasa_crecimiento_mensual": 0.01}}
    }
    
    gateway = DinamicoParametrosGateway(raw_data)
    
    inversion = gateway.get_inversion()
    assert inversion.monto_anr == 1000.0
    
    productos = gateway.get_productos()
    assert len(productos) == 1
    assert productos[0].id == "p1"
    
    lineas = gateway.get_lineas_produccion()
    assert len(lineas) == 1
    
    mix = gateway.get_mix_produccion()
    assert mix.porcentajes["p1"] == 1.0
    
    oee = gateway.get_oee_base()
    assert oee.disponibilidad == 0.1
    
    capacidad = gateway.get_capacidad_instalada()
    assert capacidad.limite_disponibilidad == 0.9
    
    escenarios = gateway.get_escenarios_raw()
    assert "test" in escenarios
