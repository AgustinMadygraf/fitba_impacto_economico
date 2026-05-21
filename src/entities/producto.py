"""
Path: src/entities/producto.py
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class Producto:
    """Representa las características económicas estáticas del producto."""
    nombre: str
    precio_unitario: float
    costos_marginales_unitarios: float

    @property
    def margen_contribucion_unitario(self) -> float:
        """Calcula el margen de contribución puro por unidad."""
        return self.precio_unitario - self.costos_marginales_unitarios
