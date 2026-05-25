# SRS - Especificación de Requerimientos del Sistema

## 1. Introducción
Este documento define los requerimientos funcionales y técnicos para el sistema de simulación de impacto económico FITBA.

## 2. Requerimientos Funcionales

### 2.1 Ajuste Financiero (Inflación)
- **RF-FIN-01:** Cálculo de valor futuro del ANR mediante interés compuesto sobre IPC.

### 2.2 Temporalidad y Referencias (RF-TEM-01) [COMPLETADO]
- El sistema debe soportar referencias calendarizadas para todas las proyecciones financieras.
- **Regla (RC-TEM-01):** La etiqueta temporal se calcula como `fecha_base + N meses`, formateada como `MM/YYYY`. 
- **Responsabilidad:** La capa de Caso de Uso debe enriquecer el resultado de la simulación con estas etiquetas antes de delegar la presentación al `JSONSimulacionPresenter`.

### 2.3 Entidades
(1:1 mapeo: Inversion, CapacidadInstalada, OEE, IndiceFinanciero, Producto, LineaProduccion, MixProduccion, Escenario).

### 2.4 Modelo de KPIs Dinámicos (RF-KPI-01)
- El OEE (Overall Equipment Effectiveness) se calcula dinámicamente como salida de la simulación.
- **OEE-Calendario**: Ratio entre Tiempo Operativo y Tiempo Total Disponible.
- **OEE-Inherente**: Ratio entre Tiempo de Valor Agregado y Tiempo Operativo.
- **Entrada**: El usuario define la "Disponibilidad Operativa" (tasa fija mensual) en lugar de un valor estático de OEE.

## 3. Restricciones Operativas
- **CapacidadInstalada (RC-OP-01):** Define la frontera máxima de producción teórica, integrando limitaciones físicas, políticas de turnos y mantenimiento preventivo necesario.
- **OEE (RC-OP-02):** Métrica de desempeño post-capacidad instalada. Cualquier valor inferior al 100% (1.0) representa ineficiencias gestionables en el uso de la capacidad definida.

### 3.1 Definiciones de Volumen
- **volumen_produccion_mensuales:** Cantidad máxima producida basada en capacidad instalada y OEE.
- **volumen_ventas_mensuales:** Cantidad efectivamente vendida, derivada de la producción ajustada por el factor de demanda del escenario.
