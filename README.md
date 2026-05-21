# FITBA - Sistema de Proyección de Impacto Económico

Herramienta en Python para calcular el incremento de eficiencia operativa (OEE) necesario para el repago del ANR otorgado a la cooperativa Madygraf.

## Resumen Ejecutivo
- **Objetivo:** Calcular el tiempo de repago (Payback Period) del ANR actualizado por inflación mediante la optimización del OEE.
- **Horizonte Temporal:** Máximo 24 meses (según GEMINI.md).
- **Stack:** Python 3.12, Clean Architecture.
- **Configuración:** Parámetros dinámicos desde data/params.json.

## Guía de Inicio Rápido
1. Ejecutar la simulación: python3 main.py.
2. Para auditoría detallada mes a mes: python3 main.py --debug.
3. Consultar GEMINI.md para las reglas de negocio y fórmulas técnicas.
