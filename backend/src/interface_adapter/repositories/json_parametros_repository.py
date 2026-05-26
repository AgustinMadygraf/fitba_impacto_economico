"""
Path: backend/src/interface_adapter/repositories/json_parametros_repository.py
"""

from src.domain.entities.operacional.capacidad_instalada import CapacidadInstalada
from src.domain.entities.entorno.escenario import Escenario
from src.domain.entities.financiero.indice_financiero import IndiceFinanciero
from src.domain.entities.financiero.inversion import Inversion
from src.domain.entities.operacional.linea_produccion import LineaProduccion
from src.domain.entities.operacional.oee import OEE
from src.domain.entities.comercial.produccion import MixProduccion
from src.domain.entities.comercial.producto import Producto
from src.domain.entities.financiero.estructura_costos import EstructuraCostos
from src.interface_adapter.repositories.parametros_gateway import ParametrosGateway

class JsonParametrosRepository(ParametrosGateway):
    def __init__(self, raw_data):
        self._data = raw_data

    def get_inversion(self) -> Inversion:
        inv_data = self._data["inversion"]
        ipc_data = self._data.get("ipc_serie", {})
        
        # Flatten IPC data for the entity
        serie = {}
        for year, months in ipc_data.get("datos", {}).items():
            for month, rate in months.items():
                serie[f"{year}-{month}"] = rate
                
        indice = IndiceFinanciero(
            nombre="IPC",
            serie_mensual=serie,
            tasa_proyectada=ipc_data.get("tasa_proyectada", 0.02)
        )
        return Inversion(inv_data["objetivo_anr"], inv_data["fecha_base"], indice)

    def get_productos(self) -> list[Producto]:
        return [Producto(
            sku=p["sku"], 
            nombre=p["nombre"], 
            precio_unitario=p["precio_unitario"],
            ancho_bolsa=p["ancho_bolsa"],
            alto_bolsa=p["alto_bolsa"],
            fuelle=p["fuelle"],
            gramaje=p["gramaje"],
            precio_bobina_kg=p["precio_bobina_kg"]
        ) for p in self._data["catalogo"]["productos"]]

    def get_lineas_produccion(self) -> list[LineaProduccion]:
        return [LineaProduccion(l["sku"], l["nombre"], l["capacidad_nominal"], l["productos_compatibles"]) for l in self._data["catalogo"]["lineas"]]

    def get_mix_produccion(self) -> MixProduccion:
        return MixProduccion({m["producto_id"]: m["porcentaje"] for m in self._data["mix_objetivo"]})

    def get_oee_base(self) -> OEE:
        oee_data = self._data["oee_base"]
        return OEE(oee_data["disponibilidad"], oee_data["rendimiento"], oee_data["calidad"])

    def get_capacidad_instalada(self) -> CapacidadInstalada:
        data = self._data["capacidad_instalada"]
        return CapacidadInstalada(
            capacidad_nominal_por_hora=data["capacidad_nominal_por_hora"],
            horas_por_turno=data["horas_por_turno"],
            turnos_por_dia=data["turnos_por_dia"],
            dias_habiles_por_mes=data["dias_habiles_por_mes"],
            dias_inhabiles_mensuales=data["dias_inhabiles_mensuales"]
        )

    def get_estructura_costos(self) -> EstructuraCostos:
        data = self._data["gestion_costos"]
        return EstructuraCostos(
            capacidad_normal_mensual=data["capacidad_normal_mensual"],
            costos_fijos_mensuales=data["costos_fijos_mensuales"],
            costo_mod_unitario=data["costo_mod_unitario"],
            costo_cif_variable_unitario=data["costo_cif_variable_unitario"]
        )

    def get_escenarios_raw(self) -> dict:
        return self._data["escenarios"]

    def get_ipc_override(self) -> float:
        return self._data.get("ipc_override")
