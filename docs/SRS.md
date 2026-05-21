# SRS - Sistema de Reporte de Impacto Económico

## Requerimientos Funcionales
1. **Cálculo de Repago:** El sistema debe determinar el incremento de OEE necesario para cubrir el ANR ($8.49M) actualizado por IPC.
2. **Entrada de Datos:** Carga de parámetros (costos, IPC, volúmenes) vía JSON.
3. **Escenarios:** Simulación de 3 contextos (Desfavorable, Proyectado, Optimista).

## Requerimientos Técnicos
1. **Lenguaje:** Python 3.12+.
2. **Arquitectura:** Clean Architecture (Separación clara de entidades, casos de uso y adaptadores).
3. **Seguridad/Git:** Los archivos JSON de datos y ejemplos no se deben trackear en el repositorio.
