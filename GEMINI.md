# Instrucciones Técnicas y Reglas de Negocio - FITBA

## Mandatos Técnicos
- **Lenguaje:** Python.
- **Patrón:** Clean Architecture.
- **Entrada:** JSON dinámico en `data/params.json`.

## Reglas de Negocio (Fuente de Verdad)
- **Target de Repago:** $8.492.000 (Solo el ANR otorgado).
- **Ajuste por Inflación:** El Target debe actualizarse a valor presente usando el factor IPC del JSON.
- **Horizonte Temporal:** 12 meses (período estático).
- **Línea Base Operativa:** 
  - Disponibilidad: 13,5% (0,135)
  - Rendimiento (Performance): 44,0% (0,44) -> **CONSTANTE**
  - Calidad (Quality): 84,0% (0,84) -> **CONSTANTE**
  - **OEE Base:** 4,99%

## Lógica de Impacto Económico (Incógnita Central)
Determinar el % de incremento necesario en la **Disponibilidad (D)** para el repago del ANR.
- **Mecánica del Beneficio:** Al mantener R y Q constantes, el beneficio económico proviene exclusivamente del **Margen de Contribución Marginal** de las unidades adicionales producidas y vendidas gracias al aumento de tiempo operativo (Disponibilidad).
- **Restricción de Demanda:** El aumento de producción efectivo está limitado por los factores de demanda definidos en cada escenario del JSON.
