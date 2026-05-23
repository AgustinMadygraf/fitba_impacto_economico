from typing import Dict, Any, List, Optional
from src.interface_adapter.repositories.parametros_gateway import ParametrosGateway
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.linea_produccion import LineaProduccion
from src.entities.produccion import MixProduccion
from src.entities.capacidad_instalada import CapacidadInstalada
from src.entities.indice_financiero import IndiceFinanciero

class JsonParametrosRepository(ParametrosGateway):
    def __init__(self, raw_data: Dict[str, Any]):
        self._raw_data = raw_data

    def get_inversion(self) -> Inversion:
        data = self._raw_data["inversion"]
        indice = None
        if "ipc_serie" in self._raw_data:
            idx_data = self._raw_data["ipc_serie"]
            serie = {int(k): v for k, v in idx_data["serie_mensual"].items()}
            indice = IndiceFinanciero(nombre=idx_data["nombre"], serie_mensual=serie, tasa_proyectada=idx_data["tasa_proyectada"])
        return Inversion(monto_anr=data["objetivo_anr"], fecha_base=data["fecha_base"], indice_base=indice)

    def get_productos(self) -> List[Producto]:
        return [Producto(id=p["id"], nombre=p["nombre"], precio_unitario=p["precio_unitario"], costo_marginal_unitario=p["costo_marginal_unitario"]) for p in self._raw_data["catalogo"]["productos"]]

    def get_lineas_produccion(self) -> List[LineaProduccion]:
        return [LineaProduccion(id=l["id"], nombre=l["nombre"], capacidad_nominal=l["capacidad_nominal"], productos_compatibles=l["productos_compatibles"]) for l in self._raw_data["catalogo"]["lineas"]]

    def get_mix_produccion(self) -> MixProduccion:
        return MixProduccion(porcentajes={m["producto_id"]: m["porcentaje"] for m in self._raw_data["mix_objetivo"]})

    def get_oee_base(self) -> OEE:
        data = self._raw_data["oee_base"]
        return OEE(disponibilidad=data["disponibilidad"], rendimiento=data["rendimiento"], calidad=data["calidad"])

    def get_capacidad_instalada(self) -> CapacidadInstalada:
        data = self._raw_data["capacidad_instalada"]
        return CapacidadInstalada(capacidad_nominal_total=data["capacidad_nominal_total_mensual"])

    def get_ipc_override(self) -> Optional[float]: return self._raw_data.get("ipc_override")
    def get_escenarios_raw(self) -> Dict[str, Any]:
        return self._raw_data["escenarios"]
