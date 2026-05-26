# SRS - FITBA Impacto Económico

## 1. Introducción
Este documento detalla los requerimientos del software de simulación financiera.

## 2. Requerimientos Funcionales
El sistema debe permitir simular el impacto económico de inversiones.

## 3. Arquitectura del Sistema

### 3.4. Capa de Servicios de Dominio
Se introduce ServicioDatosSimulacion como componente central para la obtención, filtrado y estructuración de los parámetros necesarios para la simulación. Este servicio actúa como fachada única para el caso de uso, encapsulando la lógica de negocio necesaria para consolidar:
- Precios y costos marginales (SKU).
- Parámetros operativos (OEE y Capacidad Instalada).
- Volúmenes de producción y ventas.