# DISCOVERY - Dudas e Incertidumbres Pendientes

## 1. Decisiones de Alcance (Fuera de Scope)
- **Gestión de Inventario Intermedio (Buffer):** Excluido del alcance.

## 2. Decisiones Arquitectónicas (Completadas)
- **Desacoplamiento de Entidades (Capacidad vs. OEE):** RESUELTO.
- **Persistencia Orientada al Dominio (1:1):** RESUELTO.
- **Separación de Volumen Producción/Ventas:** RESUELTO. El modelo ahora distingue conceptualmente la producción máxima (capacidad * OEE) de las ventas realizadas (producción * factor_demanda).

## 3. Estado de la Deuda Técnica
1. **Repository Pattern Abstracto:** Pendiente.
2. **Mappers Dedicados:** Pendiente.
3. **Inyección de Dependencias:** Pendiente.

## 4. Próximos Pasos (En Desarrollo)
- **Refactorización de Simulación (Ventas vs. Producción):** Refactorizar el caso de uso `SimularImpactoEconomico` para eliminar la variable consolidada `volumen_total` y reemplazarla por `volumen_produccion_mensuales` y `volumen_ventas_mensuales`.
- **Modelo de Inflación (Ajuste Financiero):** Implementar la lógica de capitalización compuesta del ANR en el Caso de Uso.

## Duda/Ambigüedad
- **Integración de Precio/Costo Marginal:** RESUELTO (Refactorización realizada).
## 4. Próximos Pasos (Refactorización)
- **Extracción a Servicios de Dominio:** Refactorizar `CasoUsoSimularImpactoEconomico` para extraer la lógica operativa (volúmenes) y financiera (inflación/valor presente) en `CalculadorImpactoOperativo` y `CalculadorImpactoFinanciero` respectivamente, aplicando el principio de Single Responsibility.
- **Extracción de Cálculo de Ingresos:** Refactorizado `CasoUsoSimularImpactoEconomico` para delegar la lógica de cálculo a `CalculadorIngresos` en `src/domain/services/`, mejorando la cohesión.