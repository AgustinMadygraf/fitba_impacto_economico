from dataclasses import dataclass

@dataclass(frozen=True)
class Producto:
    """Representa las características técnicas y económicas del producto."""
    sku: str
    nombre: str
    precio_unitario: float
    ancho_bolsa: float
    alto_bolsa: float
    fuelle: float
    gramaje: float
    precio_bobina_kg: float

    @property
    def costo_marginal_unitario(self) -> float:
        """Calcula el costo marginal unitario basándose en especificaciones técnicas."""
        ancho_bobina = (self.ancho_bolsa * 2) + (self.fuelle * 2) + 4
        longitud_corte = self.alto_bolsa + (self.fuelle / 2) + 2
        superficie_m2 = (ancho_bobina * longitud_corte) / 10000
        peso_gr = superficie_m2 * self.gramaje
        return (peso_gr / 1000) * self.precio_bobina_kg

    @property
    def margen_contribucion_unitario(self) -> float:
        """Calcula el margen de contribución puro por unidad."""
        return self.precio_unitario - self.costo_marginal_unitario
