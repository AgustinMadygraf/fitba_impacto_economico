# API Contract - FITBA Impacto Económico

Este documento define el contrato de datos entre el Backend (API REST) y el Frontend (Dashboard).

## 1. Endpoints

### GET /api/v1/simulacion/parametros
Devuelve la configuración actual del sistema utilizada para las simulaciones.

**Respuesta:**
```json
{
  "inversion": {
    "monto_anr": 8492000.0,
    "monto_actualizado": 11570350.0,
    "moneda": "ARS",
    "fecha_base": "2025-02-01",
    "fecha_objetivo": "2026-03-01"
  },
  "oee": {
    "disponibilidad": 0.135,
    "rendimiento": 0.44,
    "calidad": 0.84
  },
  "productos": [
    {
      "id": "bolsa_lisa",
      "nombre": "Bolsa Lisa",
      "precio_unitario": 150.0,
      "costo_marginal_unitario": 85.5
    }
  ],
  "mix_objetivo": {
    "bolsa_lisa": 1.0
  }
}
```

### POST /api/v1/simulacion/ejecutar
Recibe los parámetros y devuelve el resultado de la simulación.

**Cuerpo (Payload):** (Opcional, si no se envía, usa los valores por defecto del servidor).

**Respuesta:**
```json
{
  "target_repago": 11570350.0,
  "oee_base": 0.0499,
  "resultados": [
    {
      "nombre": "Desfavorable",
      "tasa": 0.01,
      "mes_repago": 18
    },
    {
      "nombre": "Proyectado",
      "tasa": 0.015,
      "mes_repago": 14
    },
    {
      "nombre": "Favorable",
      "tasa": 0.02,
      "mes_repago": 10
    }
  ]
}
```

## 2. Notas Técnicas
- **Valor Presente**: Todos los montos monetarios (`monto_actualizado`, `precio_unitario`) están expresados en moneda de hoy.
- **Tipado**: Las respuestas garantizan valores numéricos de punto flotante para los cálculos de margen y repago.
