# Guía de Negocio - FITBA

## 2. Reglas de Negocio Centralizadas
Para asegurar la consistencia, la obtención de parámetros financieros y operativos debe realizarse exclusivamente a través de los Servicios de Dominio. 

### 2.1. Consolidación de Parámetros
El sistema debe garantizar que, antes de iniciar cualquier cálculo, el ServicioDatosSimulacion valide:
- La existencia de los productos en el catálogo (via SKU).
- La compatibilidad de líneas de producción.
- La aplicación correcta de factores de OEE y capacidad instalada.## 3. Lógica de Cálculo de Costo Marginal
El costo marginal se calcula dinámicamente en base a las especificaciones técnicas.
- Ancho Bobina = (Ancho Bolsa * 2) + (Fuelle * 2) + 4cm
- Longitud Corte = Alto Bolsa + (Fuelle / 2) + 2cm
- Superficie (m2) = (Ancho Bobina * Longitud Corte) / 10000
- Peso (gr) = Superficie (m2) * Gramaje
- Costo Materia Prima = (Peso (gr) / 1000) * Precio Bobina ($/kg)
