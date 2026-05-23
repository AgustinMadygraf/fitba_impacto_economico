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
        indice = None
        if "indices" in self._raw_data and "ipc" in self._raw_data["indices"]:
            idx_data = self._raw_data["indices"]["ipc"]
            # Convertimos las llaves del dict de string a int (JSON solo soporta strings como llaves)
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
            Producto(id=p["id"], nombre=p["nombre"], precio_unitario=p["precio_unitario"], costo_marginal_unitario=p["costo_marginal_unitario"])
            for p in self._raw_data["productos"]
        ]

    def get_oee_base(self) -> OEE:
        data = self._raw_data["oee"]["linea_base"]
        return OEE(
            disponibilidad=data["disponibilidad"],
            rendimiento=data["rendimiento"],
            calidad=data["calidad"]
        )

    def get_lineas_produccion(self) -> List[LineaProduccion]:
        return [
            LineaProduccion(id=lp["id"], nombre=lp["nombre"], capacidad_nominal=lp["capacidad_nominal"], productos_compatibles=lp["productos_compatibles"])
            for lp in self._raw_data["lineas_produccion"]
        ]

    def get_mix_produccion(self) -> MixProduccion:
        porcentajes = {m["producto_id"]: m["porcentaje"] for m in self._raw_data["mix_objetivo"]}
        return MixProduccion(porcentajes=porcentajes)

    def get_capacidad_instalada(self) -> CapacidadInstalada:
        return CapacidadInstalada(
            limite_disponibilidad=self._raw_data["oee"]["limite_disponibilidad"]
        )

    def get_escenarios_raw(self) -> Dict[str, Any]:
        return self._raw_data["escenarios"]
