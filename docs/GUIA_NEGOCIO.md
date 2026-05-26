# Guía de Negocio - FITBA

## 2. Reglas de Negocio Centralizadas
Para asegurar la consistencia, la obtención de parámetros financieros y operativos debe realizarse exclusivamente a través de los Servicios de Dominio. 

### 2.1. Consolidación de Parámetros
El sistema debe garantizar que, antes de iniciar cualquier cálculo, el ServicioDatosSimulacion valide:
- La existencia de los productos en el catálogo (via SKU).
- La compatibilidad de líneas de producción.
- La aplicación correcta de factores de OEE y capacidad instalada.