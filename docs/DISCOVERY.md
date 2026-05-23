# DISCOVERY - Dudas e Incertidumbres Pendientes

## Decisiones de Alcance (Fuera de Scope)
- **Gestión de Inventario Intermedio (Buffer):** Excluido del alcance. El sistema opera bajo un modelo de flujo puro sin stock intermedio.
- **Prioridad del Backend:** El esfuerzo de desarrollo se centra exclusivamente en la precisión del modelo de costos marginales, precios de venta y la escalabilidad de costos operativos.

## 1. Modelo de Negocio
1. **Capacidad de Absorción:** ¿Se garantiza la venta del 100% incremental (Factor Demanda)?
## 3. Mejoras Arquitectónicas (Post-MVP)
1. **Centralización de Lógica de Negocio**: Migrar la lógica de cálculo de proyecciones financieras (`SimulationDomain.calculateFrontendProjections`) desde el Frontend al Backend. El Backend será la única fuente de verdad para los datasets de gráficos.
2. **Validación Dinámica**: Exponer reglas de validación (límites `gt=0`, etc.) a través del endpoint de parámetros para que la UI se configure automáticamente.
3. **Estandarización de Observabilidad**: Implementar trazas distribuidas (`X-Correlation-ID`) en todo el frontend para correlacionar errores de UI con logs de backend.


## Deuda Técnica Identificada
- **Acoplamiento de Entidades (Capacidad vs. OEE):** Actualmente, la configuración de capacidad nominal está acoplada al nodo de OEE en `params.json`.
  - *Decisión:* Se ha mantenido este acoplamiento para priorizar la estabilidad actual del sistema, pero se reconoce como deuda técnica.
  - *Acción futura:* Refactorizar la configuración para desacoplar físicamente estos dominios (Capacidad Instalada vs. Eficiencia Operativa) y actualizar los Gateways correspondientes.
