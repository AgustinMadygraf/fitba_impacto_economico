# Diseño de Arquitectura e Integración Web

## 1. Persistencia Orientada al Dominio
Mapeo 1:1 definido en `params.json`.

## 2. Responsabilidad de la Entidad: IndiceFinanciero
Calcula el factor de capitalización.

## 3. Lógica Temporal
- **Backend:** Calcula el mapeo de "Mes Relativo" (1..N) a "Fecha Absoluta" (MM/YYYY) basándose en la `fecha_base` del JSON. 
- **Frontend:** Recibe la etiqueta `MM/YYYY` ya procesada y la utiliza para renderizar tablas y gráficos, evitando lógica de fecha en el cliente.
