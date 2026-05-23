# Instrucciones Técnicas y Reglas de Negocio - FITBA

## 1. Mandatos Técnicos
- **Patrón:** Clean Architecture + DDD.
- **Persistencia Orientada al Dominio:** La configuración (`params.json`) debe mantener un mapeo **1:1** con las 8 entidades fundamentales del dominio.

## 2. Reglas de Negocio y Modelo Financiero
- **Modelo de Precio:** Operamos íntegramente a valor presente (moneda real).
- **Ajuste por Inflación (Target de Repago):**
  - El ANR es un monto nominal. El target de repago debe ajustarse mensualmente por inflación para reflejar su valor real al momento de la simulación.
  - **Fórmula de Capitalización Compuesta:** 
    - `Target_t = Target_base * \prod_{i=1}^{t} (1 + tasa_ipc_i)`
  - **Proyección de IPC:** Si el horizonte temporal (`t`) supera la serie histórica de IPC disponible, se utilizará la `tasa_proyectada` definida en la entidad `IndiceFinanciero` como constante para los meses restantes.
- **Independencia Operativa:** `CapacidadInstalada` (físico) y `OEE_Base` (operativo) son independientes. La capacidad efectiva se calcula en el Caso de Uso.

## 3. Entidades de Dominio
1. **Inversion**: ANR base.
2. **CapacidadInstalada**: Físico.
3. **OEE_Base**: Operativo.
4. **IndiceFinanciero**: Serie IPC y tasa proyectada.
5. **Productos**: Catálogo.
6. **Lineas**: Máquinas.
7. **MixObjetivo**: Configuración de producción.
8. **Escenarios**: Proyecciones de mercado.

## 4. Estándares de Calidad
- Bootstrap 100%.
- Cobertura de tests > 80%.
