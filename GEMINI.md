# Instrucciones Técnicas y Reglas de Negocio - FITBA

## 1. Mandatos Técnicos
- **Patrón:** Clean Architecture + DDD.
- **Persistencia Orientada al Dominio:** La configuración (`params.json`) debe mantener un mapeo **1:1** con las 8 entidades fundamentales.

## 2. Temporalidad y Referencias
- **Referencia Temporal Absoluta:** El sistema utiliza `fecha_base` (formato YYYY-MM-DD) provista en el nodo `inversion` del JSON como punto de anclaje.
- **Mapeo Temporal:** Todas las proyecciones (mes 1 al 24) deben ser traducidas en el backend a etiquetas absolutas con formato `MM/YYYY` antes de ser enviadas a la capa de presentación (Frontend).

## 3. Reglas de Negocio
- **Ajuste por Inflación (Target de Repago):** Ajuste mensual compuesto basado en `IndiceFinanciero`.
- **Independencia Operativa:** `CapacidadInstalada` (gestiona restricciones físicas, calendarios y límites operativos de diseño) y `OEE_Base` (gestiona métricas de eficiencia: disponibilidad operacional, rendimiento, calidad) son entidades independientes.

## 4. Estándares de Calidad
- Bootstrap 100%.
- Cobertura de tests > 80%.
## 5. Estrategia de Frontend
- Migración gradual hacia React + TypeScript.
- Testing-first: Se requiere cobertura de tests (Vitest) antes de migrar componentes.
