# Guía de Negocio - FITBA

## 1. Política de Gestión de Costos
El sistema adopta el modelo de **Costeo Completo Normalizado Integral**. Esto significa que el costo unitario de producción no se limita a los costos variables directos, sino que absorbe la totalidad de los costos operativos (fijos y variables) en función de una capacidad normal de producción predefinida.

## 2. Reglas de Negocio Centralizadas
Para asegurar la consistencia, la obtención de parámetros financieros y operativos debe realizarse exclusivamente a través de los Servicios de Dominio. 

### 2.1. Consolidación de Parámetros
El sistema debe garantizar que, antes de iniciar cualquier cálculo, el ServicioDatosSimulacion valide:
- La existencia de los productos en el catálogo (via SKU).
- La compatibilidad de líneas de producción.
- La aplicación correcta de factores de OEE y capacidad instalada.

## 3. Lógica de Cálculo de Costo Marginal
El costo marginal se calcula dinámicamente en base a las especificaciones técnicas del producto (bolsa) y el costo de la materia prima (papel).
- Ancho Bobina = (Ancho Bolsa * 2) + (Fuelle * 2) + 4cm
- Longitud Corte = Alto Bolsa + (Fuelle / 2) + 2cm
- Superficie (m2) = (Ancho Bobina * Longitud Corte) / 10000
- Peso (gr) = Superficie (m2) * Gramaje
- Costo Materia Prima = (Peso (gr) / 1000) * Precio Bobina ($/kg)

## 4. Auditoría y Trazabilidad Fiscal
El modelo permite una auditoría detallada de la formación del precio de costo. 
- **Base Técnica**: Cada costo marginal calculado se deriva de especificaciones técnicas.
- **Transparencia**: El sistema permite reconstruir el costo unitario de cualquier simulación pasada.
