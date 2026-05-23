# Instrucciones Técnicas y Reglas de Negocio - FITBA

## 1. Mandatos Técnicos
- **Rol Proactivo:** El agente opera como un consultor técnico senior.
- Lenguaje: Python.
- Patrón: Clean Architecture + DDD.
- UI Strategy: Minimizar CSS custom. Preferir clases utilitarias de Bootstrap 5.
- **Regla de Oro - Persistencia Orientada al Dominio:** La configuración del sistema (`params.json`) debe mantener un mapeo 1 a 1 con las entidades del dominio. Cada entidad fundamental debe tener su propio nodo independiente en el archivo de configuración, asegurando desacoplamiento y cohesión.

## 2. Reglas de Negocio (Fuente de Verdad)
- **Modelo de Precio y Valor Presente:** Flujos operativos a valor presente.
- **Dinamismo Financiero (Inflación):** 
  - **Target de Repago:** 8.492.000 (Monto base del ANR).
  - **Capitalización Compuesta:** Se utiliza la entidad `IndiceFinanciero` para actualizar el Target de forma exponencial mes a mes.
- **Horizonte Temporal:** Máximo 24 meses.
- **KPI de Éxito:** Repago alcanzado en < 12 meses.
- **Modelo de Producción:** Flujos independientes basados en:
  - **Capacidad Instalada:** Límite físico (independiente).
  - **OEE:** Eficiencia operativa (independiente).
  - La intersección (Capacidad Efectiva) se calcula en el Caso de Uso.

## 3. Estructura de Entidades (1:1 con Configuración)
Para mantener la independencia, el sistema mapea las siguientes 8 entidades al archivo `params.json`:
1. `inversion`
2. `capacidad_instalada`
3. `oee_base`
4. `ipc_serie`
5. `productos`
6. `lineas`
7. `mix_objetivo`
8. `escenarios`

## 4. Estándares de Calidad
- Bootstrap 100%: Layouts responsivos nativos.
- Cobertura de tests mínima: 80%.
