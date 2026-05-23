from typing import Dict, Any, List
from src.interface_adapter.repositories.parametros_gateway import ParametrosGateway
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.linea_produccion import LineaProduccion
from src.entities.produccion import MixProduccion
from src.entities.capacidad_instalada import CapacidadInstalada
from src.entities.indice_financiero import IndiceFinanciero

class DinamicoParametrosGateway(ParametrosGateway):
    def __init__(self, raw_data: Dict[str, Any]):
        self._raw_data = raw_data

    def get_inversion(self) -> Inversion:
        data = self._raw_data["inversion"]
        indice = None
        
        # Soporte para índices en el payload dinámico
        if "indices" in self._raw_data and "ipc" in self._raw_data["indices"]:
            idx_data = self._raw_data["indices"]["ipc"]
            serie = {int(k): v for k, v in idx_data["serie_mensual"].items()}
            indice = IndiceFinanciero(
                nombre=idx_data["nombre"],
                serie_mensual=serie,
                tasa_proyectada=idx_data["tasa_proyectada"]
            )
        
        return Inversion(
            monto_anr=data["objetivo_anr"],
            indice_base=indice,
            factor_correccion_inicial=data.get("factor_ipc_acumulado", 1.0)
        )

    def get_productos(self) -> List[Producto]:
        return [
            Producto(
                id=p["id"],
                nombre=p["nombre"],
                precio_unitario=p["precio_unitario"],
                costo_marginal_unitario=p["costo_marginal_unitario"]
            )
            for p in self._raw_data["productos"]
        ]

    def get_lineas_produccion(self) -> List[LineaProduccion]:
        return [
            LineaProduccion(
                id=lp["id"],
                nombre=lp["nombre"],
                capacidad_nominal=lp["capacidad_nominal"],
                productos_compatibles=lp["productos_compatibles"]
            )
            for lp in self._raw_data["lineas_produccion"]
        ]

    def get_mix_produccion(self) -> MixProduccion:
        # Manejo de mix tanto en lista como en dict para compatibilidad
        mix_data = self._raw_data["mix_objetivo"]
        if isinstance(mix_data, list):
            porcentajes = {m["producto_id"]: m["porcentaje"] for m in mix_data}
        else:
            porcentajes = mix_data
        return MixProduccion(porcentajes=porcentajes)

    def get_oee_base(self) -> OEE:
        oee_data = self._raw_data["oee"]
        if "linea_base" in oee_data:
            data = oee_data["linea_base"]
        else:
            data = oee_data
            
        return OEE(
            disponibilidad=data["disponibilidad"],
            rendimiento=data["rendimiento"],
            calidad=data["calidad"]
        )

    def get_capacidad_instalada(self) -> CapacidadInstalada:
        oee_data = self._raw_data["oee"]
        limite = oee_data.get("limite_disponibilidad", 0.85)
        return CapacidadInstalada(limite_disponibilidad=limite)

    def get_escenarios_raw(self) -> Dict[str, Any]:
        return self._raw_data["escenarios"]
