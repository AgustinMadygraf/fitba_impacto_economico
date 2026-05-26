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
- Migración gradual hacia Vue.js + TypeScript.
- Estructura: Desarrollo en paralelo (`frontend-vue/`) consumiendo la API existente (`backend/`).
- Paridad 1:1: Cada componente Vue debe replicar fielmente las funcionalidades y estructura de datos del componente legacy correspondiente.
- Dashboard UI & Chart.js Integration: Implementado y funcional.
- Migración completada: Se alcanzó paridad 1:1 con arquitectura legado, refactorizando a componentes Vue reactivos y tipados.
- Migración completada: Se alcanzó paridad 1:1 con arquitectura legado, refactorizando a componentes Vue reactivos y tipados.
- Testing-first: Se requiere cobertura de tests (Vitest) antes de migrar componentes.

## 6. Notas de Migración (Finalizada)

## 6. Notas de Migración (Finalizada)
- Se ha completado la transición del frontend legacy hacia Vue.js + TypeScript.
- La arquitectura ha pasado de manipulación imperativa del DOM a un modelo declarativo/reactivo.
- La paridad 1:1 está garantizada a nivel funcional y estético (paridad de tokens CSS).
- Funcionalidad: Se implementó `SimulationMapper.ts` para asegurar la paridad de transformación de datos (DTO) entre el frontend y el backend.
- Paridad Visual: Se implementó la estructura de grid de Bootstrap (1:1 con `index.html` legado) y se importó Bootstrap vía npm para asegurar consistencia estética.
- Funcionalidad Dinámica: Se implementaron métodos para agregar y eliminar productos y líneas de producción en tiempo real (paridad 1:1 con `simulationDashboard.js` legado).
