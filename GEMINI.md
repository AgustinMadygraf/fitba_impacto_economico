# Instrucciones Técnicas y Reglas de Negocio - FITBA

## 1. Mandatos Técnicos
- Lenguaje: Python.
- Patrón: Clean Architecture.
- Entrada: JSON dinámico en data/params.json.

## 2. Reglas de Negocio (Fuente de Verdad)
- Target de Repago: $8.492.000 (Solo el ANR otorgado).
- Ajuste por Inflación: El Target debe actualizarse a valor presente usando el factor IPC del JSON.
- Horizonte Temporal: Máximo 24 meses.
- Línea Base Operativa: 
  - Disponibilidad (D0): 13,5% (0,135)
  - Rendimiento (Performance): 44,0% (0,44) -> CONSTANTE
  - Calidad (Quality): 84,0% (0,84) -> CONSTANTE
  - OEE Base: 4,99%
  - Límite de Disponibilidad: 85% (0,85)

## 3. Lógica de Impacto Económico (Modelo Recursivo)
- Crecimiento Disponibilidad (Dt): Dt = Dt-1 * (1 + r)
- Producción Mensual (Pt): Volumen_Base * (Dt / D0)
- Beneficio Mensual (Bt): (Pt - Volumen_Base) * (Precio - Costos_Marginales_Unitarios)
- Política de Ventas: Venta Instantánea (limitada por Factor Demanda; no hay stock).
- Tasas (r): Definidas por escenario (Desfavorable, Proyectado, Favorable).
- Cálculo de Repago: Mes t donde sum(Bi) >= Inversion_Actualizada.

## 4. Decisiones de Diseño (Historial)
- Política de Ventas: Venta Instantánea (limitada por demanda).
- Margen: Margen de Contribución puro (incluye costos marginales: materia prima + energía).
- Multiplicador de Producción: Directo basado en ratio de disponibilidad (Dt/D0).
