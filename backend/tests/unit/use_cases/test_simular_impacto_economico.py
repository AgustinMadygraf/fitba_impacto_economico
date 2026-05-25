import pytest
from src.domain.entities.financiero.inversion import Inversion
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.operacional.linea_produccion import LineaProduccion
from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada
from src.domain.entities.operacional.oee import OEE
from src.domain.entities.comercial.produccion import MixProduccion
from src.domain.entities.entorno.escenario import Escenario
from src.application.simular_impacto_economico_caso_uso import CasoUsoSimularImpactoEconomico

def test_simular_impacto_repago():
    inversion = Inversion(monto_anr=1000.0, fecha_base="2025-01-01")
    productos = [Producto(id="p1", nombre="P1", precio_unitario=10.0, costo_marginal_unitario=5.0)]
    lineas = [LineaProduccion(id="l1", nombre="L1", capacidad_nominal=10000.0, productos_compatibles=["p1"])]
    capacidad = CapacidadInstalada(
        capacidad_nominal_por_hora=100.0,
        horas_por_turno=8,
        turnos_por_dia=1,
        dias_habiles_por_mes=22,
        dias_inhabiles_mensuales=1
    )
    oee = OEE(disponibilidad=0.5, rendimiento=0.5, calidad=0.5)
    mix = MixProduccion(porcentajes={"p1": 1.0})
    escenario = Escenario(nombre="Test", tasa_crecimiento=0.0, factor_demanda=1.0)
    
    use_case = CasoUsoSimularImpactoEconomico(
        inversion=inversion,
        productos=productos,
        lineas_produccion=lineas,
        capacidad_instalada=capacidad,
        mix_objetivo=mix,
        oee_base=oee,
        escenario=escenario,
        logger=None
    )
    
    mes_repago, proyeccion = use_case.ejecutar()
    assert mes_repago is not None
