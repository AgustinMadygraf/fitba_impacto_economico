# Instrucciones de Proyecto - FITBA

## Contexto y Arquitectura
- **Lenguaje:** Python.
- **Patrón:** Clean Architecture.
- **Propósito:** Refactorizar el cálculo de impacto económico centrándose en el repago del ANR.

## Reglas de Negocio
- **Target:** Recuperar $8.492.000 (ANR).
- **Inflación:** Actualizar monto por IPC a valor presente.
- **Entrada:** Los datos deben leerse de un archivo JSON en `data/`.
- **Escenarios:** El % de aumento de OEE incremental debe calcularse para 3 escenarios.

## Gestión de Archivos
- `data/*.json` y `data/*.json.example` deben permanecer untrackeados.
