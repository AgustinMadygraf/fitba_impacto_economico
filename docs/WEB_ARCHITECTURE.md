# Diseño de Arquitectura e Integración Web

Este documento define la arquitectura para el sistema FITBA, manteniendo la Clean Architecture.

## 1. Alineación de Capas (DDD)
- **Dominio (src/entities/):** Entidades puras e independientes.
- **Caso de Uso (src/use_cases/):** Orquestación y lógica de intersección (e.g., Capacidad Efectiva = Capacidad * OEE).
- **Adaptadores:** Gateways y Presenters.
- **Infraestructura:** API FastAPI y Frontend.

## 2. Persistencia Orientada al Dominio
El contrato de configuración (`params.json`) sigue un mapeo 1:1 con las entidades de dominio:
- `inversion`, `capacidad_instalada`, `oee_base`, `ipc_serie`, `catalogo (productos/lineas)`, `mix_objetivo`, `escenarios`.
- Cada Gateway debe ser responsable de cargar únicamente su entidad correspondiente, manteniendo el desacoplamiento.

## 3. API Endpoints
- **/api/v1/simulacion/parametros**: Entrega la configuración plana mapeada.
- **/api/v1/simulacion/ejecutar**: Ejecuta simulación bajo el modelo de entidades independientes.
