from dataclasses import dataclass

@dataclass(frozen=True)
class CapacidadInstalada:
    """Representa los límites físicos operativos de la planta (Físico)."""
    capacidad_nominal_total: float
