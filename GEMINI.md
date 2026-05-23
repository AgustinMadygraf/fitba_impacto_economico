# Instrucciones Técnicas y Reglas de Negocio - FITBA

## 1. Mandatos Técnicos
- **Rol Proactivo:** El agente opera como un consultor técnico senior. En cada interacción, debe proponer acciones concretas, identificar riesgos potenciales y guiar al usuario a través del roadmap, evitando estados de espera pasiva.
- Lenguaje: Python.
- Patrón: Clean Architecture.
- UI Strategy: Minimizar CSS custom. Preferir clases utilitarias de Bootstrap 5.
- Interfaz: Dashboard web con tres secciones (Entradas, Datos Intermedios, Salidas).
- Frontend: Arquitectura Clean (DDD) en JS para desacoplar lógica de la UI.

## 2. Reglas de Negocio (Fuente de Verdad)
- **Modelo de Precio y Valor Presente:** El sistema opera íntegramente a valor presente para flujos operativos. Los precios y costos están expresados en **moneda de hoy** (ya actualizados al valor presente de la simulación) y no se proyectan nominalmente; se asumen constantes en términos reales.
- **Dinamismo Financiero (Inflación):** Debido al contexto inflacionario de Argentina, el dinero tiene una asociación temporal estricta. 
  - **Target de Repago:** 8.492.000 (Monto base del ANR).
  - **Capitalización del Target:** El Target de Repago no es estático; se actualiza mes a mes durante la simulación aplicando un factor de capitalización compuesta basado en una serie de IPC (Índice de Precios al Consumidor).
  - **IPC Exponencial:** El ajuste no es lineal. Se calcula como: Target_t = Target_{t-1} * (1 + IPC_t).
- **Horizonte Temporal:** Máximo 24 meses (Límite técnico).
- **KPI de Éxito:** Repago alcanzado en menos de 12 meses.
- **Línea Base Operativa:** OEE Base 4,99%.
- **Modelo de Producción:** El sistema opera bajo "Flujos de Producción" compuestos por una o más máquinas. La capacidad efectiva de un flujo es determinada por el cuello de botella (la máquina con menor capacidad o dependencia operativa).
  - *Nota de Alcance Inicial*: El sistema se despliega restringido a un único producto y una única máquina, manteniendo la estructura extensible para futuros flujos complejos.

## 3. Diseño de Interfaz (Transparencia de Proceso)
- **Sección 1 (Entradas)**: Captura de parámetros.
- **Sección 2 (Datos Intermedios)**: Transparencia de cálculos (Target IPC Actualizado, OEE real).
- **Sección 3 (Salidas)**: Resultados y Gráficos.

## 4. Estándares de Calidad
- Bootstrap 100%: Los layouts deben ser responsivos mediante el sistema de grid nativo de Bootstrap.
