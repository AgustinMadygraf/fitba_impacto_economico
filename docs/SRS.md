# SRS - Especificación de Requerimientos del Sistema

## 1. Introducción
El sistema calculará el incremento de **Disponibilidad (D)** necesario para amortizar el ANR de Madygraf en 12 meses, manteniendo el Rendimiento y la Calidad en sus niveles base.

## 2. Entidades de Datos (Capa de Dominio)
El sistema debe gestionar las siguientes entidades core:
- **Inversión:** Monto ANR, Moneda, Fecha Base, Fecha Objetivo, Factor IPC.
- **OEE:** Disponibilidad (Variable), Rendimiento (Fijo), Calidad (Fijo).
- **Producción:** Volumen Base, Precio Unitario, Costos de Materiales, Costos Operativos por hora.
- **Escenario:** Nombre, Factor de Demanda, Factor de Ajuste de Costos.

## 3. Requerimientos Funcionales

### 3.1 Gestión de Parámetros
- **RF01:** El sistema debe cargar los parámetros desde un archivo JSON externo.
- **RF02:** Validación de Esquema: Si faltan datos obligatorios o el formato es incorrecto, el sistema debe emitir un error descriptivo.

### 3.2 Lógica de Cálculo y Simulación
- **RF03:** Actualización Financiera: El sistema debe calcular la inversión a valor presente usando el factor IPC.
- **RF04:** Modelo de Simulación: Iterar incrementos de Disponibilidad (D) para encontrar el punto de equilibrio en 12 meses.
- **RF05:** Cálculo de Beneficio: Basado exclusivamente en el Margen de Contribución de las unidades adicionales producidas (Throughput).
- **RF06:** Validación Técnica: Contrastar resultados con el límite físico de la máquina (120 bolsas/min).

### 3.3 Generación de Salidas (Outputs)
- **RF07:** Reporte Ejecutivo: Generación de un archivo Markdown con tablas comparativas.
- **RF08:** Visualización: Generación de gráficos PNG (Matplotlib) con la curva de repago.

## 4. Requerimientos No Funcionales (Atributos de Calidad)
- **RNF01 (Arquitectura):** Implementación estricta de **Clean Architecture**, **Domain-Driven Design (DDD)** y principios **SOLID**. El dominio debe estar totalmente aislado de la infraestructura.
- **RNF02 (Extensibilidad):** El sistema debe permitir añadir nuevos escenarios en el JSON sin modificar el código core.
- **RNF03 (Trazabilidad):** Registro detallado de cálculos (Logs) para auditoría.

## 5. Supuestos y Restricciones
- **S01:** El beneficio se genera por la venta de unidades excedentes.
- **S02:** La demanda máxima por escenario limita el beneficio real.
- **S03:** El horizonte de repago es de 12 meses.
