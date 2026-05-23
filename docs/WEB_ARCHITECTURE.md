# Diseño de Arquitectura e Integración Web

## 1. Persistencia Orientada al Dominio
El contrato de configuración (`params.json`) sigue un mapeo 1:1 con las 8 entidades de dominio, evitando anidamientos. Estructura base:
- `inversion`
- `capacidad_instalada`
- `oee_base`
- `ipc_serie`
- `catalogo` (contiene `productos` y `lineas`)
- `mix_objetivo`
- `escenarios`

## 2. API Endpoints
- **/api/v1/simulacion/parametros**: Entrega la configuración plana mapeada.
- **/api/v1/simulacion/ejecutar**: Recibe payload de simulación (dinámico) y retorna resultados + proyecciones.
