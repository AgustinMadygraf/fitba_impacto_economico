# Diseño de Arquitectura e Integración Web

## 1. Responsabilidad de la Entidad: IndiceFinanciero
En la Clean Architecture:
- **Dominio (`src/entities/indice_financiero.py`):** Contiene la lógica pura de capitalización (`calcular_factor_ajuste(mes: int) -> float`).
- **Caso de Uso (`src/application/simular_impacto_economico_use_case.py`):** Consume el factor de ajuste proporcionado por la entidad para actualizar el target del repago mes a mes.
- **Infraestructura:** Provee la serie IPC a través del `JsonParametrosRepository`.
