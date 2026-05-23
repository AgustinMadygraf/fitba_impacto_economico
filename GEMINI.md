# Instrucciones Técnicas y Reglas de Negocio - FITBA

## 1. Mandatos Técnicos
- **Patrón:** Clean Architecture + DDD.
- **Persistencia Orientada al Dominio (Regla de Oro):** La configuración (`params.json`) debe mantener un mapeo **1:1** con las 8 entidades fundamentales del dominio. La estructura debe ser **plana y desacoplada** para facilitar la mantenibilidad y la independencia de componentes.

## 2. Entidades de Dominio y Estructura (Fuente de Verdad)
Para garantizar la independencia física e industrial, el sistema se estructura en torno a estas 8 entidades:
1. **Inversion**: Datos financieros del ANR.
2. **CapacidadInstalada**: Límite físico (independiente).
3. **OEE_Base**: Eficiencia operativa (independiente).
4. **IPC_Serie**: Inflación acumulada (IndiceFinanciero).
5. **Productos**: Catálogo de productos.
6. **Lineas**: Catálogo de máquinas.
7. **MixObjetivo**: Configuración de producción.
8. **Escenarios**: Proyecciones de mercado.

## 3. Reglas de Negocio
- **Independencia Operativa:** La `CapacidadInstalada` (física) y el `OEE_Base` (operativo) no deben anidarse. La intersección lógica (Capacidad Efectiva) es responsabilidad exclusiva de la capa de Caso de Uso.
- **Dinamismo Financiero:** El Target de Repago se capitaliza mediante el `IndiceFinanciero` (IPC).
- **Modelo de Precio:** Operamos íntegramente a valor presente.

## 4. Estándares de Calidad
- Bootstrap 100%: Layouts responsivos nativos.
- Cobertura de tests mínima: 80%.
