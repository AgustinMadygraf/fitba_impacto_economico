# Diseño de Arquitectura e Integración Web

Este documento define la arquitectura para el sistema FITBA, manteniendo la Clean Architecture y facilitando la migración progresiva a TypeScript.

## 1. Alineación de Capas (DDD)
- Dominio (src/entities/): Entidades puras (Productos, Líneas, Mix, CapacidadInstalada, OEE, IndiceFinanciero). Las entidades de producción (Capacidad e OEE) están desacopladas para independencia de configuración.
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

## 4. Centralización de Lógica de Negocio
A partir de v1.2.2, la lógica de proyección y simulación se ha centralizado exclusivamente en el Backend.
- **Backend Responsibility:** Realiza el cálculo de beneficios mensuales, proyecciones acumuladas y determinación de viabilidad. Entrega datasets listos para graficar.
- **Frontend Responsibility:** Captura de datos de entrada (Dynamic UI), orquestación de llamadas al API y renderización de resultados (Charts y Tablas). El Frontend ya no contiene lógica de cálculo de proyecciones.

## 5. API Endpoints Principales
- **/api/v1/simulacion/parametros**: Devuelve configuración base, incluyendo `ipc_serie` para visualización en frontend.
- **/api/v1/simulacion/ejecutar**: Recibe payload de simulación (dinámico) y retorna resultados + proyecciones.
