# FITBA - Sistema de Proyección de Impacto Económico

Herramienta en Python para calcular el incremento de eficiencia operativa (OEE) necesario para el repago del ANR otorgado a la cooperativa Madygraf.

## Resumen Ejecutivo
- **Objetivo:** Determinar el % de aumento de OEE requerido para recuperar el ANR en 12 meses.
- **Stack:** Python 3.12, Clean Architecture.
- **Configuración:** Parámetros cargados desde `data/params.json` (untrackeado).

## Guía de Inicio Rápido
1. Asegurar la existencia de `data/params.json` (ver `data/params.json.example`).
2. Consultar `GEMINI.md` para las reglas de negocio y fórmulas técnicas.
3. Revisar `docs/TODO.md` para el estado del desarrollo.
