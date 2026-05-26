# SRS - FITBA Impacto Económico

## 1. Introducción
Este documento detalla los requerimientos del software de simulación financiera basado en el modelo de Costeo Completo Normalizado Integral.

## 2. Requerimientos Funcionales
El sistema debe permitir simular el impacto económico de inversiones mediante la absorción completa de costos.

## 3. Arquitectura del Sistema

### 3.4. Capa de Servicios de Dominio
Se introduce ServicioDatosSimulacion como componente central para la obtención, filtrado y estructuración de los parámetros necesarios para la simulación. 

### 3.5. Modelo de Costos Dinámicos
El sistema integra un modelo de evolución dinámica de la eficiencia productiva (OEE), permitiendo proyectar mejoras en disponibilidad, rendimiento y calidad como función de la tasa de crecimiento definida en los escenarios de simulación.
El sistema debe calcular el costo marginal unitario en tiempo de ejecución, basado en las especificaciones técnicas del producto (bolsa) y el precio de mercado de la materia prima (papel).

### 3.6. Gestión de Costos Normalizados
El sistema debe implementar el modelo de Costeo Completo, incluyendo la absorción de costos fijos y variables sobre la capacidad normal de planta, para el cálculo de costos unitarios estándar.

### 3.7. Requerimientos de Auditoría (No Funcionales)
El sistema debe garantizar la trazabilidad de los parámetros técnicos utilizados en cada simulación, permitiendo reconstruir el cálculo del costo marginal unitario para auditorías fiscales y de gestión.


### 3.8. Estrategia de Costeo (Strategy Pattern)
Para garantizar la flexibilidad y el cumplimiento de diversos estándares contables, la lógica de costeo se implementa mediante el Patrón Estrategia dentro de `src/domain/services/costeo/`. 

El sistema soporta los siguientes métodos:
1. Completo resultante por absorción.
2. Completo resultante integral.
3. Variable resultante.
4. Completo normalizado integral (Método base).
5. Variable normalizado.

Cada estrategia encapsula su propia lógica de cálculo, permitiendo al sistema adaptarse dinámicamente a distintos requerimientos de gestión sin modificar la lógica del caso de uso.


### 3.9. Mejoras de Dominio (Domain-Driven Design)
Para asegurar la robustez, el mantenimiento y la consistencia del modelo, se implementan las siguientes directrices DDD:

1. **Tipado Estricto en Costeo**: Los servicios de costeo abandonan el uso de diccionarios (`Dict`) en favor de **Value Objects** (`ParametrosCosteo`), garantizando un contrato de datos explícito y validado.
2. **Encapsulamiento de Reglas**: Se promueve la migración de cálculos dispersos a métodos de dominio dentro de las entidades (Agregados), asegurando que la lógica contable y operativa sea autovalidada.
3. **Consistencia de Agregados**: Se consolida la información técnica y de costos bajo la raíz de agregado `Producto`, permitiendo que el objeto sea autosuficiente para operaciones de simulación.


### 3.10. Módulo de Variaciones (Variances Module)
El sistema incluye un servicio de dominio `CalculadorVariaciones` para la gestión y trazabilidad contable, calculando:
- **Variación de Capacidad**: Impacto financiero de la sub/sobre-utilización de la capacidad normal de planta.
- **Variación de Eficiencia**: Desviación en el uso de recursos respecto al costo estándar unitario.
- **Variación de Volumen**: Efecto contable derivado de la diferencia entre producción y ventas reales.

Este módulo permite reconstruir las causas raíz de las desviaciones presupuestarias para auditorías fiscales y de gestión.
