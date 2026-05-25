from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class MixProduccion:
    """Representa la configuración del mix de producción objetivo."""
    porcentajes: Dict[str, float] # producto_id -> porcentaje (0.0 a 1.0)
