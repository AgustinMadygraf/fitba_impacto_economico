# SRS - Especificación de Requerimientos del Sistema

## 1. Introducción
El sistema calculará el punto de equilibrio (repago) del ANR de Madygraf en un horizonte de hasta 24 meses, aplicando las reglas de negocio definidas en GEMINI.md.

## 2. Entidades de Datos
- Inversión
- OEE Dinámico
- Producción y Finanzas
- Escenarios

## 3. Requerimientos Funcionales
- RF01: Carga y validación de parámetros (JSON).
- RF02: Simulación de impacto económico basada en el modelo recursivo definido en GEMINI.md.
- RF03: Generación de Reporte de Repago (punto de equilibrio) por escenario.
- RF04: Validación de límites físicos (Capacidad operativa máxima).

## 4. Requerimientos No Funcionales
- RNF01: Clean Architecture y DDD.
- RNF02: Extensibilidad.
