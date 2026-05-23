# TODO - FITBA Development Roadmap

## Fase 5: UI Dinámica y Tipado Progresivo (Prioridad Alta)
- [ ] Implementar UI para Gestión Dinámica de Productos y Líneas (RF11).
  - *Nota*: Restringir inicialmente a 1 Producto, 1 Máquina.
- [ ] Refactorización de componentes para soporte multiproducto (Preparación extensible).

## Fase 6: Centralización de Lógica y Observabilidad (Post-MVP)
- [ ] Implementar cálculo de proyecciones mensuales (trayectoria de beneficio) en el Backend (`SimularImpactoEconomico`).
- [ ] Exponer datasets de proyecciones a través de `/api/v1/simulacion/ejecutar`.
- [ ] Migrar lógica de `SimulationDomain` (Frontend) para consumir datasets del Backend.
- [ ] Implementar `CorrelationID` en frontend para mejorar trazabilidad de errores (Observabilidad).
