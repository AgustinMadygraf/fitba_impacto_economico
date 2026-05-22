"""
Path: src/interface_adapter/gateway/dinamico_gateway.py
"""

from typing import Dict, Any
from src.interface_adapter.gateway.parametros_gateway import ParametrosGateway
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import Produccion
from src.entities.capacidad_instalada import CapacidadInstalada

class DinamicoParametrosGateway(ParametrosGateway):
    """
    Gateway adaptador que toma un diccionario de datos dinámico
    (enviado desde la API web o frontend) y construye las entidades de dominio FITBA.
    """
    
    def __init__(self, raw_data: Dict[str, Any]):
        self._raw_data = raw_data

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
