# TODO - FITBA Development Roadmap

## Integración de Interfaz Web (FastAPI + HTML + Bootstrap + JS)
- [ ] **Fase 1: Servidor y API (FastAPI Backend)**
  - [ ] Implementar el servidor FastAPI en `src/infrastructure/web/app.py` y configurar Uvicorn.
  - [ ] Desarrollar esquemas Pydantic de entrada/salida para la validación estricta del payload.
  - [ ] Implementar endpoint `GET /api/params` para leer la configuración por defecto.
  - [ ] Implementar endpoint `POST /api/simular` para recibir parámetros variables del frontend y simular dinámicamente.
- [ ] **Fase 2: Adaptadores de Arquitectura Limpia**
  - [ ] Crear `JSONSimulacionPresenter` bajo `src/interface_adapter/presenter/` que implemente la interfaz `SimulacionPresenter` para formatear los resultados en diccionarios JSON.
  - [ ] Implementar un adaptador de parámetros dinámicos (`RequestParametrosGateway`) para alimentar el controlador desde el JSON recibido en la request HTTP.
- [ ] **Fase 3: Interfaz de Usuario Premium (Bootstrap 5 + JS)**
  - [ ] Diseñar el dashboard responsivo en `index.html` bajo `src/infrastructure/web/static/` utilizando Bootstrap 5.
  - [ ] Crear la hoja de estilos `custom.css` aplicando el "Wow Factor" (diseño oscuro elegante, paneles glassmorphism, tipografía moderna, sutiles micro-animaciones al interactuar con inputs y botones).
  - [ ] Implementar la lógica del cliente en `app.js` usando Fetch API para invocar de forma asíncrona la simulación al modificar los inputs.
  - [ ] Integrar Chart.js para dibujar dinámicamente la evolución de la disponibilidad del OEE y las curvas de beneficios de los 3 escenarios.
  - [ ] Añadir controles únicos de ID a los campos de entrada para garantizar la testeabilidad automática.

## Próximos Pasos (Evolución del Motor)
- [ ] **Implementar Mix de Productos:** Soporte para múltiples tipos de productos (Revistas, Folletos, Libros) con márgenes diferenciados.
- [ ] **Refinamiento de Costo Marginal:** Incluir prorrateo dinámico de energía y evaluación de necesidad de horas extra según volumen.
- [ ] **Pruebas de Estrés de Capacidad:** Verificación de comportamiento del sistema ante saturación de disponibilidad máxima (85%).
- [ ] **Persistencia de Resultados:** Opción para exportar el reporte a un archivo (CSV/JSON) para análisis posterior.

