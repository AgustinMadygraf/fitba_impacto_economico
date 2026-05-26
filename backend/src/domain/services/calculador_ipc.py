"""
Path: backend/src/domain/services/calculador_ipc.py
"""

from datetime import datetime
from src.domain.entities.financiero.indice_financiero import IndiceFinanciero

class CalculadorIPC:
    @staticmethod
    def calculate_factor(indice: IndiceFinanciero, fecha_base: str, fecha_objetivo: datetime) -> float:
        base = datetime.strptime(fecha_base, "%Y-%m-%d")
        months_diff = (fecha_objetivo.year - base.year) * 12 + (fecha_objetivo.month - base.month)
        return indice.calcular_factor_capitalizacion(max(0, months_diff))
