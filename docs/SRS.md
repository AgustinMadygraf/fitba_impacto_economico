# SRS - Especificación de Requerimientos del Sistema

## 1. Introducción
El sistema calculará el punto de equilibrio (repago) del ANR de Madygraf en un horizonte de hasta 24 meses, aplicando las reglas de negocio definidas en GEMINI.md.

## 2. Entidades de Datos
- Inversión
- OEE Dinámico
- Producción y Finanzas
- Escenarios

## 3. Requerimientos Funcionales
- **RF01:** Carga y validación de parámetros por defecto (JSON).
- **RF02:** Simulación de impacto económico basada en el modelo recursivo definido en GEMINI.md.
- **RF03:** Generación de Reporte de Repago (punto de equilibrio) por escenario.
- **RF04:** Validación de límites físicos (Capacidad operativa máxima).
- **RF05:** Interfaz Gráfica de Usuario (Web Dashboard): Dashboard interactivo y responsivo optimizado para desktop y mobile.
- **RF06:** Formulario de Simulación Dinámica: Permitir al usuario modificar en tiempo real todos los parámetros operativos y financieros (montos, IPC, OEE base, costos marginales, precios y tasas) y disparar simulaciones al instante sin reiniciar el servicio.
- **RF07:** Visualización Gráfica Interactiva: Representación gráfica de la evolución mensual de la disponibilidad del OEE y las curvas de beneficio acumulado por escenario (utilizando Chart.js o similar).
- **RF08:** API REST (FastAPI): Endpoint `GET /api/params` para servir la configuración base y `POST /api/simular` para calcular proyecciones con payloads variables.

## 4. Requerimientos No Funcionales
- **RNF01:** Clean Architecture y DDD (Domain-Driven Design).
- **RNF02:** Extensibilidad e independencia de frameworks.
- **RNF03:** Experiencia de Usuario de Alto Rendimiento (Wow Factor): Interfaz construida con Bootstrap 5, paleta oscura premium, efectos glassmorphism, micro-animaciones en interacciones y tiempos de respuesta de la API menores a 50ms.
- **RNF04:** Aislamiento del Framework de Entrega: FastAPI, Jinja2 y cualquier biblioteca frontend quedarán estrictamente confinados en la capa de Infraestructura, sin filtrar dependencias hacia las entidades o casos de uso.

