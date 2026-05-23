# SRS - Especificación de Requerimientos del Sistema

## 1. Ajuste Financiero (Inflación)
El sistema debe ajustar el Target de Repago utilizando un modelo de interés compuesto basado en la serie IPC proporcionada.

- **Requerimiento Funcional (RF-FIN-01):** El sistema debe leer la serie de tasas mensuales de IPC y calcular el valor futuro del ANR para cada mes del horizonte de simulación (hasta 24 meses).
- **Regla de Cálculo (RC-FIN-01):** 
  - Para meses dentro de la serie IPC: `Target_t = Target_{t-1} * (1 + ipc_t)`.
  - Para meses fuera de la serie IPC: `Target_t = Target_{t-1} * (1 + tasa_proyectada)`.
- **Requerimiento no Funcional (RNF-FIN-01):** La entidad `IndiceFinanciero` debe ser la única responsable de calcular el factor de ajuste dado un mes específico, garantizando encapsulamiento.

## 2. Entidades Principales
(Como definido en el modelo 1:1, incluyendo `IndiceFinanciero` con las reglas anteriores).
