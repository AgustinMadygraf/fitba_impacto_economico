class CalculadorVariaciones:
    @staticmethod
    def calcular_variacion_capacidad(capacidad_normal: float, capacidad_real: float, tasa_cif_fijos: float) -> float:
        """Impacto de sub/sobre-utilización de la capacidad instalada."""
        return (capacidad_normal - capacidad_real) * tasa_cif_fijos

    @staticmethod
    def calcular_variacion_eficiencia(costo_estandar_unitario: float, costo_real_unitario: float, produccion_real: float) -> float:
        """Impacto de desviaciones en el uso de insumos/recursos."""
        return (costo_estandar_unitario - costo_real_unitario) * produccion_real

    @staticmethod
    def calcular_variacion_volumen(produccion_real: float, ventas_reales: float, costo_fijo_absorbido: float) -> float:
        """Impacto contable de la diferencia entre lo producido y lo vendido."""
        return (produccion_real - ventas_reales) * costo_fijo_absorbido
