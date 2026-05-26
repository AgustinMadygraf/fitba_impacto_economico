# SRS - FITBA Impacto Económico

## 1. Introducción
Este documento detalla los requerimientos del software de simulación financiera.

## 2. Requerimientos Funcionales
El sistema debe permitir simular el impacto económico de inversiones.

## 3. Arquitectura del Sistema

### 3.4. Capa de Servicios de Dominio
Se introduce ServicioDatosSimulacion como componente central para la obtención, filtrado y estructuración de los parámetros necesarios para la simulación. 

### 3.5. Modelo de Costos Dinámicos
El sistema debe calcular el costo marginal unitario en tiempo de ejecución, basado en las especificaciones técnicas del producto (bolsa) y el precio de mercado de la materia prima (papel).
