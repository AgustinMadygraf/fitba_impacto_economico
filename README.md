# FITBA - Sistema de Proyección de Impacto Económico

Herramienta en Python bajo Clean Architecture para calcular el repago del ANR otorgado a Madygraf mediante optimización de OEE.

## Resumen Ejecutivo
- **Objetivo:** Determinar la viabilidad del repago en un horizonte de 12 meses (KPI de éxito).
- **Límite Técnico:** Simulación de hasta 24 meses.
- **Transparencia:** Interfaz web organizada en tres capas: Entradas, Datos Intermedios y Salidas.

## Guía de Inicio Rápido
1. Consultar `GEMINI.md` para reglas de negocio.
2. Ejecutar simulación CLI: `python3 main.py`.
3. Servidor Web: Consultar `WEB_ARCHITECTURE.md`.

## Funcionalidades Recientes
- **Modelo de Inflación:** Ajuste automático del Target de Repago utilizando capitalización compuesta mensual.
- **Anclaje Temporal (Calendar-Based):** Soporte completo para fechas absolutas (MM/YYYY) derivado de una `fecha_base` configurable, permitiendo referencias temporales precisas en todas las proyecciones financieras.
