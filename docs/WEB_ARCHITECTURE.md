# Diseño de Arquitectura e Integración Web

Este documento define la arquitectura para el sistema FITBA, manteniendo la Clean Architecture y facilitando la migración progresiva a TypeScript.

## 1. Alineación de Capas (DDD)
- Dominio (src/entities/): Entidades puras (Productos, Líneas, Mix). Sin dependencias.
- Casos de Uso (src/use_cases/): Lógica de simulación.
- Adaptadores (src/interface_adapter/): Gateways y Presenters.
- Infraestructura (src/infrastructure/): API FastAPI y Frontend JS/TS.

## 2. Estrategia de Migración a TypeScript
Para evitar una reescritura traumática, seguiremos estos pasos:
1. JSDoc Estricto: Todo código JS nuevo debe usar @typedef y @type para definir interfaces.
2. Interfaz de Dominio: Centralizar tipos en la capa de dominio.
3. Conversión .js -> .ts: Renombrado incremental cuando los tipos JSDoc sean maduros.

## 3. Decisiones Técnicas (Resueltas)
- **Stack Tecnológico:** Uso de Chart.js vía CDN para visualización y FastAPI para el backend.
