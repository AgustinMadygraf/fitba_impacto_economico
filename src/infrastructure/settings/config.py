"""
Path: src/infrastructure/settings/config.py
"""

import json
from typing import Dict, Any
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import Produccion
from src.entities.capacidad_instalada import CapacidadInstalada

class ConfigLoader:
    """
    Cargador de configuración de infraestructura.
    Se encarga de transformar los parámetros crudos (JSON) en Entidades de Dominio.
    """
    
    def __init__(self, config_path: str = "data/params.json"):
        self.config_path = config_path
        self._raw_data = self._load_json()

    def _load_json(self) -> Dict[str, Any]:
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get_inversion(self) -> Inversion:
        data = self._raw_data['inversion']
        return Inversion(
            monto_anr=data['objetivo_anr'],
            factor_ipc=data['factor_ipc_acumulado']
        )

    def get_producto(self) -> Producto:
        data = self._raw_data['produccion']
        return Producto(
            nombre="Producto Genérico Madygraf",
            precio_unitario=data['precio_unitario_promedio'],
            costos_marginales_unitarios=data['costos_variables']['material_por_unidad']
        )

    def get_oee_base(self) -> OEE:
        data = self._raw_data['oee']['linea_base']
        return OEE(
            disponibilidad=data['disponibilidad'],
            rendimiento=data['rendimiento'],
            calidad=data['calidad']
        )

    def get_produccion_base(self) -> Produccion:
        vol_base = self._raw_data['produccion']['volumen_mensual_base']
        return Produccion(
            volumen_base=vol_base,
            volumen_vector=[vol_base]
        )

    def get_capacidad_instalada(self) -> CapacidadInstalada:
        return CapacidadInstalada(
            limite_disponibilidad=self._raw_data['oee']['limite_disponibilidad']
        )

    def get_escenarios_raw(self) -> Dict[str, Any]:
        return self._raw_data['escenarios']
