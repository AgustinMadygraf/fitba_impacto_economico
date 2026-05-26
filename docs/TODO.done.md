# Tareas Completadas - FITBA

- [x] **Fase 1: Servidor y API (FastAPI Backend)**
- [x] **Fase 2: Adaptadores de Arquitectura Limpia**
- [x] **Fase 3: Refactorización a Bootstrap Estándar (Migración Progresiva)**
  - [x] **Paso 3.1: Layout**
  - [x] **Paso 3.2: Componentes**
  - [x] **Paso 3.3: Tipografía**
  - [x] **Paso 3.4: Theme**
- [x] Implementar Mix de Productos

- [x] **Fase 4: Refactorización Frontend (Clean Architecture)**
  - [x] Paso 4.1-4.4: Estructura base DDD aplicada

- [x] **Fase 5: UI Dinámica y Tipado Progresivo**
  - [x] Instrumentar tipado JSDoc estricto en nuevos módulos
  - [x] Implementar UI para Gestión Dinámica de Productos y Líneas (RF11)
  - [x] Refactorización de componentes para soporte multiproducto (Preparación extensible)

- [x] **Fase 6: Centralización de Lógica y Observabilidad (Post-MVP)**
  - [x] Centralización de ejecución: implementado 'run.sh' como único punto de entrada
  - [x] Unificación: eliminación de 'backend/run_web.py'
  - [x] Implementar cálculo de proyecciones mensuales (trayectoria de beneficio) en el Backend (`SimularImpactoEconomico`)
  - [x] Exponer datasets de proyecciones a través de `/api/v1/simulacion/ejecutar`
  - [x] Migrar lógica de `SimulationDomain` (Frontend) para consumir datasets del Backend (Eliminación de redundancia)
  - [x] Implementar `CorrelationID` en frontend y backend para mejorar trazabilidad de errores (Observabilidad)
- [x] Implementar UI en la sección de Entradas para visualizar/editar la serie de IPC
- [x] Refactorización: Centralización de cálculo de IPC en `IPCCalculator` (Servicio de Dominio)
- [x] Corrección de KPIs: Refactorización de cálculo de `monto_anr_real` y visualización centralizada
- [x] **Arquitectura Dinámica de IPC**: Implementación de modelo basado solo en datos observados con proyección automática por backend- [x] Desacoplar `limite_disponibilidad` de `OEE` y mover a `CapacidadInstalada`.

- [x] **Fase 7: OEE Dinámico y Sensibilidad a Escenarios**
  - [x] Implementar evolución dinámica de componentes de OEE (Disponibilidad, Rendimiento, Calidad).
  - [x] Integrar factores de mejora de OEE en la entidad `Escenario`.
  - [x] Refactorizar `SimularImpactoEconomico` para utilizar la lógica dinámica de OEE del dominio.

- [x] **Fase 8: Implementación de Estrategias de Costeo (Patrón Estrategia)**
  - [x] Crear interfaz `EstrategiaCosteo`.
  - [x] Implementar `CompletoResultanteAbsorcion`.
  - [x] Implementar `CompletoResultanteIntegral`.
  - [x] Implementar `VariableResultante`.
  - [x] Implementar `CompletoNormalizadoIntegral`.
  - [x] Implementar `VariableNormalizado`.

- [x] **Fase 8: Implementación del Módulo de Variaciones**
  - [x] Implementar servicio `CalculadorVariaciones` con cálculos de capacidad, eficiencia y volumen.
