# Diseño de Arquitectura e Integración Web (FastAPI + Bootstrap 5 + JS)

Este documento define la especificación técnica detallada para integrar un dashboard web interactivo en el sistema FITBA. La implementación respeta estrictamente los principios de **Clean Architecture**, asegurando que el motor de simulación de impacto económico permanezca aislado de los detalles de entrega (FastAPI) y presentación (Bootstrap/HTML/JS).

---

## 1. Alineación de Capas (Clean Architecture)

```mermaid
graph TD
    subgraph Infraestructura (Periferia)
        FastAPI[FastAPI Server: app.py]
        HTML[UI: index.html]
        CSS[Styling: custom.css]
        JS[Logic: app.js]
    end

    subgraph Adaptadores de Interfaz
        Gateway[RequestParametrosGateway]
        Presenter[JSONSimulacionPresenter]
        Controller[SimulacionController]
    end

    subgraph Casos de Uso (Núcleo)
        UseCase[SimularImpactoEconomico]
    end

    subgraph Entidades (Dominio)
        Inversion[Inversion]
        OEE[OEE]
        Produccion[Produccion]
        Producto[Producto]
        Escenario[Escenario]
    end

    %% Relaciones de dependencia (apuntan hacia el centro)
    FastAPI --> Controller
    FastAPI --> Gateway
    FastAPI --> Presenter
    
    Controller --> UseCase
    Controller --> Gateway
    Controller --> Presenter
    
    UseCase --> Inversion
    UseCase --> OEE
    UseCase --> Produccion
    UseCase --> Producto
    UseCase --> Escenario
```

- **Capa de Dominio (`src/entities/`)**: **Inmutable.** No se permite la importación de libreráas externas o dependencias del framework web.
- **Capa de Casos de Uso (`src/use_cases/`)**: **Inmutable.** Sigue ejecutando la simulación basada en el modelo recursivo puro.
- **Capa de Adaptadores de Interfaz (`src/interface_adapter/`)**:
  - `JSONSimulacionPresenter`: Nueva clase que implementa la interfaz `SimulacionPresenter`. Almacena en memoria el resultado formateado como un diccionario JSON estándar de Python.
  - `RequestParametrosGateway`: Nueva clase que adapta los parámetros recibidos mediante el cuerpo de la petición HTTP (JSON) a las entidades de dominio requeridas.
- **Capa de Infraestructura (`src/infrastructure/web/`)**:
  - Aloja el servidor web FastAPI (`app.py`), el enrutador de la API, y los recursos estáticos.

---

## 2. Flujo de Control en una Petición Web

El siguiente diagrama muestra la secuencia detallada desde que el usuario pulsa "Ejecutar Simulación" en el frontend hasta que se renderizan los resultados en pantalla.

```mermaid
sequenceDiagram
    autonumber
    actor Usuario
    participant JS as Frontend (app.js)
    participant API as FastAPI (app.py)
    participant Gateway as RequestParametrosGateway
    participant Presenter as JSONSimulacionPresenter
    participant Controller as SimulacionController
    participant UseCase as SimularImpactoEconomico

    Usuario->>JS: Clic en "Ejecutar Simulación"
    JS->>API: HTTP POST /api/simular (JSON Payload)
    activate API
    API->>Gateway: Instanciar con datos de Request
    API->>Presenter: Instanciar JSONSimulacionPresenter
    API->>Controller: Instanciar SimulacionController(Gateway, Presenter)
    API->>Controller: ejecutar_simulacion()
    activate Controller
    Controller->>Gateway: get_inversion(), get_producto(), etc.
    Gateway-->>Controller: Entidades de Dominio
    
    loop Para cada escenario (Desfavorable, Proyectado, Favorable)
        Controller->>UseCase: Instanciar SimelarImpactoEconomico(...)
        Controller->>UseCase: ejecutar()
        activate UseCase
        UseCase-->>Controller: Mes de repago (int o None)
        deactivate UseCase
    end
    
    Controller->>Presenter: presentar_resultados(target, oee_base, resultados)
    activate Presenter
    Note over Presenter: Convierte a DTO serializable<br/>y lo guarda en self.response_data
    Presenter-->>Controller: Ok
    deactivate Presenter
    Controller-->>API: Ok
    deactivate Controller
    
    API-->>JS: HTTP 200 OK (JSON Response)
    deactivate API
    activate JS
    Note over JS: Actualiza tablas y<br/>redibuja Chart.js
    JS-->>Usuario: Visualización del Dashboard Actualizado
    deactivate JS
```mermaid
sequenceDiagram
    autonumber
    actor Usuario
    participant JS as Frontend (app.js)
    participant API as FastAPI (app.py)
    participant Gateway as RequestParametrosGateway
    participant Presenter as JSONSimulacionPresenter
    participant Controller as SimulacionController
    participant UseCase as SimularImpactoEconomico

    Usuario->>JS: Clic en "Ejecutar Simulación"
    JS->>API: HTTP POST /api/simular (JSON Payload)
    activate API
    API->>Gateway: Instanciar con datos de Request
    API->>Presenter: Instanciar JSONSimulacionPresenter
    API->>Controller: Instanciar SimulacionController(Gateway, Presenter)
    API->>Controller: ejecutar_simulacion()
    activate Controller
    Controller->>Gateway: get_inversion(), get_producto(), etc.
    Gateway-->>Controller: Entidades de Dominio
    
    loop Para cada escenario (Desfavorable, Proyectado, Favorable)
        Controller->>UseCase: Instanciar SimelarImpactoEconomico(...)
        Controller->>UseCase: ejecutar()
        activate UseCase
        UseCase-->>Controller: Mes de repago (int o None)
        deactivate UseCase
    end
    
    Controller->>Presenter: presentar_resultados(target, oee_base, resultados)
    activate Presenter
    Note over Presenter: Convierte a DTO serializable<br/>y lo guarda en self.response_data
    Presenter-->>Controller: Ok
    deactivate Presenter
    Controller-->>API: Ok
    deactivate Controller
    
    API-->>JS: HTTP 200 OK (JSON Response)
    deactivate API
    activate JS
    Note over JS: Actualiza tablas y<br/>redibuja Chart.js
    JS-->>Usuario: Visualización del Dashboard Actualizado
    deactivate JS
```

---

## 3. Especificación del Backend (FastAPI)

### Ubicación del Código
- Archivo principal: [app.py](file:///home/agustin/proyectos_software/fitba_impacto_economico/src/infrastructure/web/app.py)
- Carpeta de estáticos: [static/](file:///home/agustin/proyectos_software/fitba_impacto_economico/src/infrastructure/web/static/)

### Estructura de Datos (Esquema de Entrada)
Se utilizará **Pydantic** para validar que los valores ingresados cumplan los límites operativos.

```python
from pydantic import BaseModel, Field

class OEEBaseInput(BaseModel):
    disponibilidad: float = Field(0.135, ge=0.01, le=1.0)
    rendimiento: float = Field(0.44, ge=0.01, le=1.0)
    calidad: float = Field(0.84, ge=0.01, le=1.0)

class ProduccionInput(BaseModel):
    volumen_mensual_base: float = Field(450000.0, gt=0)
    precio_unitario_promedio: float = Field(150.0, gt=0)
    costo_material_unitario: float = Field(85.5, ge=0)

class InversionInput(BaseModel):
    objetivo_anr: float = Field(8492000.0, gt=0)
    factor_ipc_acumulado: float = Field(1.3625, ge=1.0)

class EscenarioInput(BaseModel):
    tasa_crecimiento_mensual: float = Field(..., ge=0.0, le=1.0)
    factor_demanda: float = Field(1.0, ge=0.0, le=2.0)

class SimulationRequest(BaseModel):
    inversion: InversionInput
    oee: OEEBaseInput
    produccion: ProduccionInput
    escenarios: dict[str, EscenarioInput]
```

### Rutas de la API (Endpoints)
1. `GET /api/params`: Retorna los valores de `data/params.json` para pre-completar los campos de la interfaz.
2. `POST /api/simular`: Ejecuta la simulación basándose en los parámetros del payload.
3. `GET /`: Sirve el archivo estático `index.html`.

---

## 4. Adaptadores de Interfaz (Implementación)

### JSON Presenter
Permite capturar la llamada del controlador y guardarla en formato JSON.

```python
from src.interface_adapter.presenter.simulacion_presenter import SimulacionPresenter

class JSONSimulacionPresenter(SimulacionPresenter):
    def __init__(self):
        self.response_data = {}

    def presentar_resultados(self, target_repago: float, oee_base: float, resultados: list):
        self.response_data = {
            "exito": True,
            "target_repago": target_repago,
            "oee_base": oee_base,
            "resultados": [
                {
                    "escenario": res["nombre"],
                    "tasa": res["tasa"],
                    "mes_repago": res["mes_repago"],
                    "viable": res["mes_repago"] is not None and res["mes_repago"] <= 24
                }
                for res in resultados
            ]
        }
```

---

## 5. Diseño del Frontend (Wow Factor)

La interfaz se construirá con un enfoque **Mobile First** y diseño **Premium Dashboard**, organizada en tres secciones funcionales claras para mejorar la interpretabilidad de los datos.

### Estructura de Tres Secciones

1.  **Sección de Entradas (Variables de Control):**
    - Controles interactivos para modificar los parámetros de inversión, OEE base, producción y escenarios.
    - Ubicación: Panel lateral (Sidebar) o sección superior.
    - Propósito: Permitir al usuario "jugar" con las variables del modelo.

2.  **Sección de Datos Intermedios (Cálculos de Proceso):**
    - Visualización de valores derivados que conectan las entradas con los resultados finales.
    - Incluye:
        - Inversión Actualizada (Valor Presente ajustado por IPC).
        - OEE Base Calculado (D0 × Performance × Calidad).
        - Margen de Contribución Unitario.
        - Capacidad Máxima Operativa.
    - Propósito: Proporcionar transparencia sobre cómo el motor transforma las entradas.

3.  **Sección de Salidas (Resultados y Visualización):**
    - Resultados finales de la simulación.
    - Incluye:
        - Tabla de Análisis de Repago (Payback) por escenario.
        - Indicadores de Viabilidad (Semáforos).
        - Gráfico Interactivo de Curvas de Proyección Financiera (Chart.js).
    - Propósito: Facilitar la toma de decisiones basada en los resultados finales.

### Estética y Experiencia de Usuario
- **Glassmorphic Cards**: Bordes finos y semitransparentes con sombra suave y filtro de desenfoque (`backdrop-filter: blur(12px)`).
- **Interactive Form Inputs**: Transiciones al enfocar (`focus`) ampliando ligeramente el campo y agregando un brillo neon sutil.
- **Micro-animaciones**:
  - Los botones tendrán efectos hover con transiciones CSS de 0.2 segundos.
  - Spinner de carga personalizado para el estado de cálculo.
- **Visualización Progresiva**: Los datos intermedios y de salida se actualizan automáticamente al cambiar cualquier entrada (Debounce asíncrono).

### Paleta de Colores (HSL Tailored CSS Variables)
```css
:root {
  --bg-dark: hsl(220, 25%, 8%);
  --bg-panel: hsla(220, 25%, 12%, 0.75);
  --border-glass: hsla(220, 25%, 25%, 0.4);
  --text-primary: hsl(220, 20%, 95%);
  --text-secondary: hsl(220, 15%, 70%);
  --accent-blue: hsl(195, 100%, 50%);      /* Neon Blue para proyectado */
  --accent-green: hsl(145, 80%, 45%);       /* Emerald Green para favorable */
  --accent-orange: hsl(25, 95%, 50%);       /* Sunset Orange para desfavorable */
  --btn-gradient: linear-gradient(135deg, hsl(195, 100%, 45%), hsl(145, 80%, 40%));
}
```

### Estructura HTML y Testeabilidad (IDs Únicos)
Para garantizar la compatibilidad con frameworks de pruebas automatizadas, todos los campos de entrada y controles clave tendrán IDs únicos y semánticos:

| Elemento | ID de Control | Propósito |
| :--- | :--- | :--- |
| **Input Inversión ANR** | `input-anr` | Captura el ANR base |
| **Input Factor IPC** | `input-ipc` | Ajuste por inflación |
| **Input Disponibilidad (D0)** | `input-disp-base` | Línea base del OEE |
| **Input Rendimiento** | `input-perf` | Rendimiento constante |
| **Input Calidad** | `input-quality` | Calidad constante |
| **Input Vol. Base** | `input-vol-base` | Producción de referencia |
| **Input Precio Venta** | `input-precio` | Precio por unidad |
| **Input Costo Unitario** | `input-costo` | Costos marginales base |
| **Botón Simular** | `btn-simular` | Dispara el cálculo REST |
| **Tabla Resultados** | `table-resultados` | Contenedor de la grilla final |
| **Lienzo Gráfico** | `chart-proyeccion` | Canvas para el gráfico Chart.js |

---

## 6. Siguientes Pasos
Una vez resueltas las dudas listadas en [DISCOVERY.md](file:///home/agustin/proyectos_software/fitba_impacto_economico/docs/DISCOVERY.md), se procederá a:
1. Instalar dependencias (`fastapi`, `uvicorn`, `pydantic`).
2. Crear la estructura de directorios para estático  en `src/infrastructure/web/`.
3. Implementar el backend de FastAPI y probar los endpoints vía Swagger UI (`/docs`).
4. Desarrollar la interfaz frontend de alto impacto visual.
