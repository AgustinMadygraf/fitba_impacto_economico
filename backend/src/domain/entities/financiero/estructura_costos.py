"""
Path: backend/src/domain/entities/financiero/estructura_costos.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class EstructuraCostos:
    """Representa la estructura de costos para el modelo de absorción."""
    capacidad_normal_mensual: float
    costos_fijos_mensuales: float
    costo_mod_unitario: float
    costo_cif_variable_unitario: float

    @property
    def tasa_absorcion_fijos(self) -> float:
        """Calcula la tasa de absorción de costos fijos por unidad."""
        return self.costos_fijos_mensuales / self.capacidad_normal_mensual
