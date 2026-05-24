from dataclasses import dataclass

@dataclass(frozen=True)
class CapacidadInstalada:
    """Representa los límites físicos operativos de la planta (Físico)."""
    capacidad_nominal_por_hora: float
    horas_por_turno: int
    turnos_por_dia: int
    dias_habiles_por_mes: int
    dias_inhabiles_mensuales: int

    @property
    def capacidad_nominal_total(self) -> float:
        """Calcula la capacidad nominal total mensual basado en turnos y días."""
        dias_operativos = self.dias_habiles_por_mes - self.dias_inhabiles_mensuales
        return self.capacidad_nominal_por_hora * self.horas_por_turno * self.turnos_por_dia * dias_operativos
