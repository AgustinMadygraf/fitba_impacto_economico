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
from src.interface_adapter.gateway.parametros_gateway import ParametrosGateway

# Capturar tiempo al importar el módulo (inicio del proceso)
_START_TIME = datetime.datetime.now().isoformat()

class ConfigLoader(ParametrosGateway):
    def __init__(self, config_path: str = "data/params.json"):
        if os.path.isabs(config_path):
            self.config_path = config_path
        else:
            self.config_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", config_path)
        self._args = self._parse_cli_args()
        self._raw_data = self._load_json()
