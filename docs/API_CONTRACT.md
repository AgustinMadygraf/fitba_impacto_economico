# API Contract - FITBA Impacto Económico

Este documento define el contrato de datos entre el Backend (API REST) y el Frontend (Dashboard).

## 1. Endpoints

### GET /api/v1/simulacion/parametros
Devuelve la configuración actual del sistema utilizada para las simulaciones. El cálculo del valor real ajustado por inflación se realiza centralizadamente en el backend para garantizar la integridad financiera.

**Respuesta:**
```json
{
  "inversion": {
    "monto_anr_nominal": 8492000.0,
    "monto_anr_real": 12900000.0,
    "fecha_base": "2025-02-01",
    "ipc_acumulado": 1.52
  },
  "disponibilidad_operativa_target": 0.95,
  "productos": [],
  "ipc_serie": [],
  "tasa_proyectada": 0.02
}
```

### POST /api/v1/simulacion/ejecutar
Recibe los parámetros y devuelve el resultado de la simulación.

**Respuesta:**
```json
{
  "target_repago": 8492000.0,
  "kpis": {
    "oee_calendario": 0.85,
    "oee_inherente": 0.92
  },
  "resultados": [],
  "proyecciones": {
    "proyectado": []
  }
}
```

## 2. Notas Técnicas
- **Valor Presente**: El backend calcula `monto_anr_real` como fuente de verdad (`monto_anr_nominal * ipc_acumulado`). El frontend consume este valor para su visualización.
- **IPC Acumulado**: El campo `ipc_acumulado` es una instantánea (snapshot) dinámica calculada por el backend, representando el factor acumulado desde la `fecha_base` de la inversión hasta la fecha actual, derivado exclusivamente de la serie histórica y proyectada proporcionada en el JSON de configuración (fuente única de verdad).
- **Modelo de Datos IPC (`params.json`)**: El objeto `ipc_serie.datos` contiene exclusivamente datos observados (históricos). Para cualquier mes no presente en la serie histórica, el motor financiero aplica automáticamente `tasa_proyectada` para calcular la inflación a futuro.