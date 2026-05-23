# SRS - Especificación de Requerimientos del Sistema

## 1. Introducción
El sistema calculará el punto de equilibrio (repago) del ANR de Madygraf.

**Horizontes Temporales:**
- **Límite de Simulación:** Hasta 24 meses (capacidad técnica del motor).
- **KPI de Éxito:** Repago alcanzado en menos de 12 meses.

## 2. Entidades de Datos
- Inversión
- OEE Dinámico
- Producción y Finanzas
- Escenarios
- Productos (Mix)
- Líneas de Producción (Mapping)

## 3. Requerimientos Funcionales
- **RF01:** Carga y validación de parámetros por defecto (JSON).
- **RF02:** Simulación de impacto económico basada en el modelo recursivo definido en GEMINI.md.
- **RF03:** Generación de Reporte de Repago (punto de equilibrio) por escenario.
- **RF04:** Validación de límites físicos (Capacidad operativa máxima).
- **RF05:** Interfaz Gráfica de Usuario (Web Dashboard): Dashboard interactivo organizado en tres secciones funcionales (Entradas, Datos Intermedios y Salidas).
- **RF06:** Formulario de Simulación Dinámica (Sección Entradas): Ajuste en tiempo real de parámetros operativos y financieros.
- **RF07:** Visualización de Datos Intermedios (Sección Datos Intermedios): Mostrar cálculos derivados (Inversión Actualizada, OEE Base real, Márgenes) para transparencia del modelo.
- **RF08:** Visualización Gráfica Interactiva (Sección Salidas): Resultados finales de repago, viabilidad y curvas de beneficio acumulado (Chart.js).
- **RF09:** API REST (FastAPI): Endpoints para servir parámetros base y procesar simulaciones dinámicas.
- **RF10:** Cálculo Multiproducto: El motor de simulación debe calcular el beneficio mensual ponderando el volumen producido según la configuración de mix de productos de cada ítem.
- **RF11:** Gestión de Mix de Productos en Interfaz: Sección 1 debe permitir configurar productos, precios, costos y mix.
- **RF12:** Mapeo Línea-Producto: La interfaz debe permitir asignar líneas de producción (máquinas) a productos específicos para una estimación de capacidad más precisa.

## 4. Requerimientos No Funcionales
- **RNF01:** Clean Architecture y DDD.
- **RNF02:** Independencia de frameworks.
- **RNF03:** UX Premium (Wow Factor): Bootstrap 5, glassmorphism, micro-animaciones y respuesta < 50ms.
- **RNF04:** Aislamiento de Infraestructura: Capas de dominio y casos de uso sin dependencias de FastAPI o librerías frontend.