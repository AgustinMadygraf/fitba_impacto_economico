from src.entities.capacidad_instalada import CapacidadInstalada
from src.entities.escenario import Escenario
from src.entities.indice_financiero import IndiceFinanciero
from src.entities.inversion import Inversion
from src.entities.linea_produccion import LineaProduccion
from src.entities.oee import OEE
from src.entities.produccion import MixProduccion
from src.entities.producto import Producto
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
        return [Producto(p["id"], p["nombre"], p["precio_unitario"], p["costo_marginal_unitario"]) for p in self._data["catalogo"]["productos"]]

    def get_lineas_produccion(self) -> list[LineaProduccion]:
        return [LineaProduccion(l["id"], l["nombre"], l["capacidad_nominal"], l["productos_compatibles"]) for l in self._data["catalogo"]["lineas"]]

    def get_mix_produccion(self) -> MixProduccion:
        return MixProduccion({m["producto_id"]: m["porcentaje"] for m in self._data["mix_objetivo"]})

    def get_oee_base(self) -> OEE:
        oee_data = self._data["oee_base"]
        return OEE(oee_data["disponibilidad"], oee_data["rendimiento"], oee_data["calidad"])

    def get_capacidad_instalada(self) -> CapacidadInstalada:
        return CapacidadInstalada(self._data["capacidad_instalada"]["capacidad_nominal_total_mensual"])

    def get_escenarios_raw(self) -> dict:
        return self._data["escenarios"]

    def get_ipc_override(self) -> float:
        return self._data.get("ipc_override")
