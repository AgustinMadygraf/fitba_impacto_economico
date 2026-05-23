# Instrucciones Técnicas y Reglas de Negocio - FITBA

## 1. Mandatos Técnicos
- Lenguaje: Python.
- Patrón: Clean Architecture.
- UI Strategy: Minimizar CSS custom. Preferir clases utilitarias de Bootstrap 5.
- Interfaz: Dashboard web con tres secciones (Entradas, Datos Intermedios, Salidas).
- Frontend: Arquitectura Clean (DDD) en JS para desacoplar lógica de la UI.

## 2. Reglas de Negocio (Fuente de Verdad)
- Target de Repago: .492.000 (Solo el ANR otorgado).
- Ajuste por Inflación: El Target debe actualizarse a valor presente usando el factor IPC del JSON.
- Horizonte Temporal: Máximo 24 meses (Límite técnico).
- Línea Base Operativa: OEE Base 4,99%.
- **Modelo de Producción:** El sistema opera bajo "Flujos de Producción" compuestos por una o más máquinas. La capacidad efectiva de un flujo es determinada por el cuello de botella (la máquina con menor capacidad o dependencia operativa).
- **Dependencias Operativas:** Se soportan flujos secuenciales (donde una máquina A es necesaria para que B funcione).

## 3. Diseño de Interfaz (Transparencia de Proceso)
- **Sección 1 (Entradas)**: Captura de parámetros.
- **Sección 2 (Datos Intermedios)**: Transparencia de cálculos (Target IPC, OEE real).
- **Sección 3 (Salidas)**: Resultados y Gráficos.

## 4. Estándares de Calidad
- Bootstrap 100%: Los layouts deben ser responsivos mediante el sistema de grid nativo de Bootstrap.