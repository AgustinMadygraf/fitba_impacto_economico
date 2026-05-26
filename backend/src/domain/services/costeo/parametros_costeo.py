from dataclasses import dataclass

@dataclass(frozen=True)
class ParametrosCosteo:
    costos_fijos_totales: float = 0.0
    produccion_real: float = 1.0
    cif_variables_totales: float = 0.0
    cif_fijos_totales: float = 0.0
