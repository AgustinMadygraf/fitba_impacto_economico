from typing import Dict, Any, List
from src.interface_adapter.gateway.parametros_gateway import ParametrosGateway
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.linea_produccion import LineaProduccion
from src.entities.produccion import MixProduccion
from src.entities.capacidad_instalada import CapacidadInstalada

class DinamicoParametrosGateway(ParametrosGateway):
    def __init__(self, raw_data: Dict[str, Any]):
        self._raw_data = raw_data

    def get_inversion(self) -> Inversion:
        data = self._raw_data["inversion"]
        return Inversion(
            monto_anr=data["objetivo_anr"],
            factor_ipc=data["factor_ipc_acumulado"]
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
        porcentajes = {m["producto_id"]: m["porcentaje"] for m in self._raw_data["mix_objetivo"]}
        return MixProduccion(porcentajes=porcentajes)

    def get_oee_base(self) -> OEE:
        # Aceptamos la nueva estructura plana o la antigua para compatibilidad
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
        # Valor por defecto si no se envía, manteniendo compatibilidad
        limite = oee_data.get("limite_disponibilidad", 0.85)
        return CapacidadInstalada(
            limite_disponibilidad=limite
        )

    def get_escenarios_raw(self) -> Dict[str, Any]:
        return self._raw_data["escenarios"]
