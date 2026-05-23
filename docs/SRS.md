# SRS - Especificación de Requerimientos del Sistema

## 1. Entidades de Dominio (Mapeo 1:1 con Configuración)
Para asegurar el desacoplamiento, la configuración del sistema refleja explícitamente estas 8 entidades:
1. **Inversion**: Datos financieros del ANR.
2. **CapacidadInstalada**: Límite físico (independiente de OEE).
3. **OEE**: Eficiencia operativa (independiente de capacidad).
4. **IndiceFinanciero (IPC)**: Inflación acumulada.
5. **Producto**: Catálogo de productos.
6. **LineaProduccion**: Catálogo de máquinas.
7. **MixProduccion**: Configuración de producción.
8. **Escenario**: Proyecciones de mercado.

## 2. Decisiones Técnicas
- **Desacoplamiento Industrial:** `CapacidadInstalada` y `OEE` se tratan como entes físicos y operativos independientes, calculando la capacidad efectiva exclusivamente en el Caso de Uso.
- **Persistencia Orientada al Dominio:** La configuración JSON es plana y refleja 1 a 1 las 8 entidades del dominio para facilitar la mantenibilidad.
