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
