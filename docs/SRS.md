# SRS - FITBA Impacto Económico

## 1. Introducción
Este documento detalla los requerimientos del software de simulación financiera basado en el modelo de Costeo Completo Normalizado Integral.

## 2. Requerimientos Funcionales
El sistema debe permitir simular el impacto económico de inversiones mediante la absorción completa de costos.

## 3. Arquitectura del Sistema

### 3.4. Capa de Servicios de Dominio
Se introduce ServicioDatosSimulacion como componente central para la obtención, filtrado y estructuración de los parámetros necesarios para la simulación. 

### 3.5. Modelo de Costos Dinámicos
El sistema debe calcular el costo marginal unitario en tiempo de ejecución, basado en las especificaciones técnicas del producto (bolsa) y el precio de mercado de la materia prima (papel).

### 3.6. Gestión de Costos Normalizados
El sistema debe implementar el modelo de Costeo Completo, incluyendo la absorción de costos fijos y variables sobre la capacidad normal de planta, para el cálculo de costos unitarios estándar.

### 3.7. Requerimientos de Auditoría (No Funcionales)
El sistema debe garantizar la trazabilidad de los parámetros técnicos utilizados en cada simulación, permitiendo reconstruir el cálculo del costo marginal unitario para auditorías fiscales y de gestión.
