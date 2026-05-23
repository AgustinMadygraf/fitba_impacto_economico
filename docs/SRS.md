# SRS - Especificación de Requerimientos del Sistema

## 1. Introducción
El sistema calculará el punto de equilibrio (repago) del ANR de Madygraf, considerando el valor del dinero en el tiempo debido a la inflación.

**Horizontes Temporales:**
- **Límite de Simulación:** Hasta 24 meses.
- **KPI de Éxito:** Repago alcanzado en menos de 12 meses.

**Alcance Inicial:**
- El sistema se despliega restringido a un único producto y una única máquina, manteniendo la estructura extensible para futuros flujos complejos.

## 2. Entidades de Datos
- **Inversión**: Datos financieros del ANR.
- **Índice Financiero (IPC)**: Serie temporal de inflación intermensual para capitalización del target.
- **Capacidad Instalada**: Límites físicos operativos (independiente de la eficiencia).
- **OEE**: Factores de eficiencia operativa (independiente de la capacidad instalada).
- **Líneas de Producción**: Definición de máquinas y productos compatibles.
- **Productos**: Definición de márgenes de contribución.
- **Mix Objetivo**: Configuración de producción por producto.
- **Escenarios**: Proyecciones de mercado (Tasa de crecimiento, factor de demanda).

## 3. Requerimientos Funcionales
- **RF01**: Carga y validación de parámetros vía API REST.
- **RF02**: Simulación de impacto económico basada en el modelo recursivo con **capitalización compuesta del target**.
- **RF03**: Reporte de Repago por escenario.
- **RF04**: Validación de límites físicos (Capacidad operativa).
- **RF05**: Web Dashboard interactivo (Frontend DDD).
- **RF06**: Formulario de Simulación Dinámica (Entradas).
- **RF07**: Visualización de Datos Intermedios (Evolución del Target IPC, OEE Real).
- **RF08**: Visualización Gráfica (Chart.js): El Backend entrega los datasets procesados (proyecciones calculadas); el Frontend solo se encarga de la renderización visual.
- **RF09**: API REST (FastAPI).
- **RF10**: Cálculo Multiproducto: Ponderación de volumen por Mix Objetivo.
- **RF11**: Gestión de Productos y Líneas (Dinámico): CRUD básico de productos, líneas y su asociación en el mix.
- **RF12**: Modelado de Flujos Productivos: Cálculo de capacidad efectiva basado en la intersección independiente de Capacidad Instalada y factores OEE.

## 4. Requerimientos No Funcionales
- **RNF01**: Clean Architecture y DDD.
- **RNF02**: Independencia de frameworks.
- **RNF03**: UX Premium (Bootstrap 5, micro-animaciones).
- **RNF04**: Preparación para TypeScript (JSDoc estricto en JS).

## 5. Decisiones Técnicas (Resueltas)
- **Estrategia de Testing:** Framework pytest con estructura por capas (unit/integration) y cobertura mínima del 80%.
- **Infraestructura CI:** Uso de hooks de git locales (pre-push.sh) como primera barrera de calidad.
- **Desacoplamiento de Producción:** Se ha formalizado la separación entre *Capacidad Instalada* (física) y *OEE* (eficiencia), tratándolos como entidades de dominio independientes para mejorar la modelización.
- **Lógica de Inflación Exponencial:** El sistema utiliza una entidad `IndiceFinanciero` que aplica tasas mensuales sobre el target de inversión de forma acumulativa para determinar el punto de equilibrio real.
- **Naturaleza de los Productos:** Se reconoce que los productos son variables y el precio de referencia es una abstracción para el cálculo del punto de equilibrio inicial.
