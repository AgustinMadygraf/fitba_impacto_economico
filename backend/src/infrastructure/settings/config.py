import json
import argparse
import os
import datetime
from typing import Dict, Any, List

from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.linea_produccion import LineaProduccion
from src.entities.produccion import MixProduccion
from src.entities.capacidad_instalada import CapacidadInstalada
from src.entities.indice_financiero import IndiceFinanciero
from src.interface_adapter.repositories.parametros_gateway import ParametrosGateway

_START_TIME = datetime.datetime.now().isoformat()

class ConfigLoader(ParametrosGateway):
    def __init__(self, config_path: str = "data/params.json"):
        if os.path.isabs(config_path):
            self.config_path = config_path
        else:
            self.config_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", config_path)
        self._args = self._parse_cli_args()
        self._raw_data = self._load_json()

    def _parse_cli_args(self):
        parser = argparse.ArgumentParser(description="Simulador de Impacto Económico FITBA")
        parser.add_argument("--debug", action="store_true", help="Habilitar modo auditoría técnica (DEBUG)")
        return parser.parse_known_args()[0]

    def get_app_mode(self) -> str:
        return os.getenv("APP_MODE", "development")

    def get_start_time(self) -> str:
        return _START_TIME

    def is_debug_enabled(self) -> bool:
        return self._args.debug

    def _load_json(self) -> Dict[str, Any]:
        with open(self.config_path, "r") as f:
            return json.load(f)

    def get_inversion(self) -> Inversion:
        data = self._raw_data["inversion"]
        indice_data = self._raw_data.get("ipc_serie")
        indice = None
        if indice_data:
            serie = {int(k): v for k, v in indice_data["serie_mensual"].items()}
            indice = IndiceFinanciero(
                nombre=indice_data["nombre"],
                serie_mensual=serie,
                tasa_proyectada=indice_data["tasa_proyectada"]
            )
        return Inversion(monto_anr=data["objetivo_anr"], indice_base=indice)

    def get_productos(self) -> List[Producto]:
        return [
            Producto(id=p["id"], nombre=p["nombre"], precio_unitario=p["precio"], costo_marginal_unitario=p["costo"])
            for p in self._raw_data["catalogo"]["productos"]
        ]

    def get_oee_base(self) -> OEE:
        data = self._raw_data["oee_base"]
        return OEE(disponibilidad=data["disponibilidad"], rendimiento=data["rendimiento"], calidad=data["calidad"])

    def get_lineas_produccion(self) -> List[LineaProduccion]:
        return [
            LineaProduccion(id=l["id"], nombre=l["nombre"], capacidad_nominal=l["capacidad_nominal"], productos_compatibles=l["productos_compatibles"])
            for l in self._raw_data["catalogo"]["lineas"]
        ]

    def get_mix_produccion(self) -> MixProduccion:
        return MixProduccion(porcentajes={m["producto_id"]: m["porcentaje"] for m in self._raw_data["mix_objetivo"]})

    def get_capacidad_instalada(self) -> CapacidadInstalada:
        data = self._raw_data["capacidad_instalada"]
        return CapacidadInstalada(capacidad_nominal_total=data["capacidad_nominal_total_mensual"])

    def get_escenarios_raw(self) -> Dict[str, Any]:
        return self._raw_data["escenarios"]
