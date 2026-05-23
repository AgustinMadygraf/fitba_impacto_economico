# SRS - Especificación de Requerimientos del Sistema

## 1. Introducción
El sistema calculará el punto de equilibrio (repago) del ANR de Madygraf.

**Horizontes Temporales:**
- **Límite de Simulación:** Hasta 24 meses.
- **KPI de Éxito:** Repago alcanzado en menos de 12 meses.

**Alcance Inicial:**
- El sistema se despliega restringido a un único producto y una única máquina, manteniendo la estructura extensible para futuros flujos complejos.

## 2. Entidades de Datos
- **Inversión**: Datos financieros del ANR.
- **OEE Dinámico**: Parámetros operativos (Disponibilidad, Rendimiento, Calidad).
- **Líneas de Producción**: Definición de capacidad instalada y productos compatibles.
- **Productos**: Definición de márgenes de contribución.
- **Mix Objetivo**: Configuración de producción por producto.
- **Escenarios**: Proyecciones de mercado (Tasa de crecimiento, factor de demanda).

## 3. Requerimientos Funcionales
- **RF01**: Carga y validación de parámetros vía API REST.
- **RF02**: Simulación de impacto económico basada en el modelo recursivo.
- **RF03**: Reporte de Repago por escenario.
- **RF04**: Validación de límites físicos (Capacidad operativa).
- **RF05**: Web Dashboard interactivo (Frontend DDD).
- **RF06**: Formulario de Simulación Dinámica (Entradas).
- **RF07**: Visualización de Datos Intermedios (Inversión Actualizada, OEE Real).
- **RF08**: Visualización Gráfica (Chart.js): El Backend entrega los datasets procesados (proyecciones calculadas); el Frontend solo se encarga de la renderización visual.
- **RF09**: API REST (FastAPI).
- **RF10**: Cálculo Multiproducto: Ponderación de volumen por Mix Objetivo. (*MVP*: Limitado a 1 producto; Arquitectura: Diseñada para extender a multiproducto).
- **RF11**: Gestión de Productos y Líneas (Dinámico): CRUD básico de productos, líneas y su asociación en el mix.
- **RF12**: Modelado de Flujos Productivos: Cálculo de capacidad efectiva. (*MVP*: Limitado a 1 máquina; Arquitectura: Diseñada para implementar cuello de botella).

## 4. Requerimientos No Funcionales
- **RNF01**: Clean Architecture y DDD.
- **RNF02**: Independencia de frameworks.
- **RNF03**: UX Premium (Bootstrap 5, micro-animaciones).
- **RNF04**: Preparación para TypeScript (JSDoc estricto en JS).

## 5. Decisiones Técnicas (Resueltas)
- **Estrategia de Testing:** Framework pytest con estructura por capas (unit/integration) y cobertura mínima del 80%.
- **Infraestructura CI:** Uso de hooks de git locales (pre-push.sh) como primera barrera de calidad.
- **Lógica de IPC y Valor Presente:** El sistema opera bajo un modelo de valor presente. El factor IPC se aplica **exclusivamente** sobre la inversión inicial para establecer el "Target" actualizado. Los precios y costos marginales ya se encuentran expresados en moneda de hoy y se consideran constantes en términos reales durante la simulación de 24 meses.
- **Naturaleza de los Productos:** Se reconoce que los productos son variables y el precio de referencia es una abstracción para el cálculo del punto de equilibrio inicial.
