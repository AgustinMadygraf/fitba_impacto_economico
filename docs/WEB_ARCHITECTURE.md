# Diseño de Arquitectura e Integración Web

## 1. Persistencia Orientada al Dominio
Mapeo 1:1 definido en `params.json`.

## 2. Responsabilidad de la Entidad: IndiceFinanciero
Calcula el factor de capitalización.

## 3. Lógica Temporal
- **Backend:** Calcula el mapeo de "Mes Relativo" (1..N) a "Fecha Absoluta" (MM/YYYY) basándose en la `fecha_base` del JSON. 
- **Frontend:** Recibe la etiqueta `MM/YYYY` ya procesada y la utiliza para renderizar tablas y gráficos, evitando lógica de fecha en el cliente.

## 4. Evolución Frontend: Migración a React + TypeScript
El frontend actual se está refactorizando para mejorar su observabilidad y preparar la migración hacia React + TypeScript.
- **Estrategia:** Testing-first. Se implementará un framework de tests (Vitest) antes de realizar cambios estructurales en el código.
- **Flujo de Migración:** 
  1. Configuración de tests.
  2. Migración del sistema de construcción a Vite.
  3. Definición de contratos de datos compartidos (TS).
  4. Portado progresivo de componentes.


## 5. Principio de Capa de Infraestructura Delgada (Thin Infrastructure Layer)
Para mantener el desacoplamiento:
- Las rutas web (`routes.py`) **solo** deben gestionar la recepción de peticiones HTTP y la delegación a controladores.
- Cualquier lógica de transformación de datos (DTOs, formateo JSON) **debe** delegarse a un `Presenter`.
- Cualquier lógica de negocio, cálculo o agregación de datos **debe** delegarse al Dominio o a Servicios de Aplicación.
- Está terminantemente prohibido implementar lógica de cálculo en `routes.py`.


- Se debe utilizar **Inyección de Dependencias (FastAPI Depends)** para instanciar controladores, repositorios o servicios, evitando la instanciación manual dentro de las funciones de ruta. Esto promueve la desacoplación y facilita las pruebas unitarias de los componentes.

## 6. Mapeo y Orquestación (Clean Architecture)
- **Mapper de Payload**: Toda transformación de esquemas de API (Pydantic/DTO) a estructuras internas del repositorio debe encapsularse en un `Mapper` especializado (Interface Adapter Layer).
- **Controladores Delgado**: Los controladores (`SimulacionController`) orquestan la ejecución y el mapeo, eliminando lógica de transformación de la capa de rutas.
- **Inyección de Dependencias**: Utilizar `FastAPI.Depends` para proveer controladores y servicios, evitando instanciación manual dentro de las funciones de ruta.
