# Instrucciones Técnicas y Reglas de Negocio - FITBA

## 1. Mandatos Técnicos
- Lenguaje: Python.
- Patrón: Clean Architecture.
- UI Strategy: Minimizar CSS custom. Preferir clases utilitarias de Bootstrap 5.
- Interfaz: Dashboard web con tres secciones (Entradas, Datos Intermedios, Salidas).

## 2. Reglas de Negocio (Fuente de Verdad)
- Target de Repago: .492.000 (Solo el ANR otorgado).
- Ajuste por Inflación: El Target debe actualizarse a valor presente usando el factor IPC del JSON.
- Horizonte Temporal: Máximo 24 meses (Límite técnico).
- Línea Base Operativa: OEE Base 4,99%.
- **Mix de Productos:** El modelo soporta n productos. Cada producto define su propio `precio_unitario` y `costos_marginales_unitarios`.
- **Relación Línea-Producto:** Cada línea de producción (máquina) es asignable a uno o más productos. El beneficio mensual se calcula como la sumatoria de las contribuciones ponderadas de la producción total del mix.

## 3. Diseño de Interfaz (Transparencia de Proceso)
- **Sección 1 (Entradas)**: Captura de parámetros.
- **Sección 2 (Datos Intermedios)**: Transparencia de cálculos (Target IPC, OEE real).
- **Sección 3 (Salidas)**: Resultados y Gráficos.

## 4. Estándares de Calidad
- Bootstrap 100%: Los layouts deben ser responsivos mediante el sistema de grid nativo de Bootstrap.