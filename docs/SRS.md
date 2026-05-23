# SRS - Especificación de Requerimientos del Sistema

## 1. Ajuste Financiero (Inflación)
- **RF-FIN-01:** Cálculo de valor futuro del ANR mediante interés compuesto sobre IPC.

## 2. Temporalidad y Referencias (RF-TEM-01) [COMPLETADO]
- El sistema debe soportar referencias calendarizadas para todas las proyecciones financieras.
- **Regla (RC-TEM-01):** La etiqueta temporal se calcula como `fecha_base + N meses`, formateada como `MM/YYYY`. 
- **Responsabilidad:** La capa de Caso de Uso debe enriquecer el resultado de la simulación con estas etiquetas antes de delegar la presentación al `JSONSimulacionPresenter`.

## 3. Entidades
(1:1 mapeo: Inversion, CapacidadInstalada, OEE, IndiceFinanciero, Producto, LineaProduccion, MixProduccion, Escenario).
