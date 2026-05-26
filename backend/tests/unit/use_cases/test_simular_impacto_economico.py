"""
Path: backend/tests/unit/use_cases/test_simular_impacto_economico.py
"""

from unittest.mock import MagicMock
from src.domain.entities.financiero.inversion import Inversion
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada
from src.domain.entities.operacional.oee import OEE
from src.domain.entities.comercial.produccion import MixProduccion
from src.domain.entities.entorno.escenario import Escenario
from src.application.simular_impacto_economico_caso_uso import CasoUsoSimularImpactoEconomico
from src.domain.services.servicio_datos_simulacion import ServicioDatosSimulacion

def test_simular_impacto_repago():
    inversion = Inversion(monto_anr=1000.0, fecha_base="2025-01-01")
    producto = Producto(
        sku="p1", 
        nombre="P1", 
        precio_unitario=10.0, 
        ancho_bolsa=10.0,
        alto_bolsa=10.0,
        fuelle=5.0,
        gramaje=100.0,
        precio_bobina_kg=2.0
    )
    capacidad = CapacidadInstalada(
        capacidad_nominal_por_hora=100.0,
        horas_por_turno=8,
        turnos_por_dia=1,
        dias_habiles_por_mes=22,
        dias_inhabiles_mensuales=1
    )
    oee = OEE(disponibilidad=0.5, rendimiento=0.5, calidad=0.5)
    mix = MixProduccion(porcentajes={"p1": 1.0})
    escenario = Escenario(nombre="Test", tasa_disponibilidad=0.0, tasa_rendimiento=0.0, tasa_calidad=0.0, factor_demanda=1.0)
    
    # Mock ServicioDatosSimulacion
    servicio_datos = MagicMock(spec=ServicioDatosSimulacion)
    servicio_datos.obtener_productos_mapeados.return_value = {"p1": producto}
    servicio_datos.obtener_oee.return_value = oee
    servicio_datos.obtener_capacidad.return_value = capacidad
    
    use_case = CasoUsoSimularImpactoEconomico(
        servicio_datos=servicio_datos,
        inversion=inversion,
        mix_objetivo=mix,
        escenario=escenario,
        logger=None
    )
    
    mes_repago, proyeccion = use_case.ejecutar()
    assert mes_repago is not None
