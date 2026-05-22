# FITBA - Sistema de Proyección de Impacto Económico

Herramienta en Python para calcular el incremento de eficiencia operativa (OEE) necesario para el repago del ANR otorgado a la cooperativa Madygraf.

## Resumen Ejecutivo
- **Objetivo:** Calcular el tiempo de repago (Payback Period) del ANR actualizado por inflación mediante la optimización del OEE.
- **Horizonte Temporal:** Máximo 24 meses (según GEMINI.md).
- **Stack:** Python 3.12, Clean Architecture.
- **Configuración:** Parámetros dinámicos desde data/params.json.

## Guía de Inicio Rápido
1. Ejecutar la simulación CLI: `python3 main.py`.
2. Para auditoría detallada mes a mes en CLI: `python3 main.py --debug`.
3. Consultar `GEMINI.md` para las reglas de negocio y fórmulas técnicas.

## Próxima Evolución: Interfaz de Usuario Web
Se incorporará un servidor de entrega web utilizando **FastAPI** y una interfaz interactiva dinámica de alto rendimiento (**HTML + Bootstrap 5 + Vanilla Javascript**) para permitir simulaciones y ajustes de parámetros en tiempo real.

### Alineación Arquitectónica (Clean Architecture)
El framework web y el motor de renderizado residen estrictamente en la periferia del sistema, garantizando la independencia y reusabilidad del motor de cálculo:
- **Infraestructura (`src/infrastructure/web/`)**: Contiene la definición del servidor FastAPI, validaciones de esquemas Pydantic y los archivos frontend estáticos (`index.html`, `custom.css`, `app.js`).
- **Adaptador de Presentación (`src/interface_adapter/presenter/`)**: Un nuevo `JSONSimulacionPresenter` implementará la interfaz abstracta `SimulacionPresenter` para formatear los resultados de la simulación en una estructura JSON apta para la API REST.
- **Adaptador de Entrada (`src/interface_adapter/gateway/`)**: Un adaptador dinámico interpretará las peticiones HTTP cargando los valores ingresados por el usuario como entidades de dominio puras para los casos de uso.

