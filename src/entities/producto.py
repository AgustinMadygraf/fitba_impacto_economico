from dataclasses import dataclass

@dataclass(frozen=True)
class Producto:
    """Representa las características económicas estáticas del producto."""
    id: str
    nombre: str
    precio_unitario: float
    costo_marginal_unitario: float

    @property
    def margen_contribucion_unitario(self) -> float:
        """Calcula el margen de contribución puro por unidad."""
        return self.precio_unitario - self.costo_marginal_unitario
