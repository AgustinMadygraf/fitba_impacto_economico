# DISCOVERY - Dudas e Incertidumbres Pendientes

## Decisiones de Alcance (Fuera de Scope)
- **Gestión de Inventario Intermedio (Buffer):** Excluido del alcance. El sistema opera bajo un modelo de flujo puro sin stock intermedio.
- **Prioridad del Backend:** El esfuerzo de desarrollo se centra exclusivamente en la precisión del modelo de costos marginales, precios de venta y la escalabilidad de costos operativos.

## 1. Modelo de Negocio
1. **Mix de Ventas:** ¿Cómo se distribuye el mix de producción? ¿Es constante o varía con el volumen?
2. **Capacidad de Absorción:** ¿Se garantiza la venta del 100% incremental (Factor Demanda)?
3. **Costos de Escalamiento:** ¿A partir de qué volumen el costo de hora operativa (12.000) requiere la apertura de nuevos turnos?
4. **Estandarización de Impresoras:** ¿La "Impresora de Bolsas" dedicada tiene la misma velocidad/capacidad que la "Impresora en línea"?

## 2. Interfaz Web de Tres Secciones
1. **Reactividad vs. Botón:** ¿La actualización de las secciones "Datos Intermedios" y "Salidas" debe ser automática al cambiar un input (Debounce) o requiere pulsar "Ejecutar Simulación"?
2. **Profundidad de Datos Intermedios:** ¿La Sección 2 debe incluir una tabla con el desglose mensual (traza de auditoría) o solo los KPI consolidados?
3. **Persistencia de Parámetros:** ¿Los ajustes realizados por el usuario en la "Sección de Entradas" deben persistir en localStorage para futuras sesiones o ser volátiles?
4. **Seguridad de Acceso:** Dado el carácter sensible de los costos de la cooperativa, ¿se requiere autenticación básica o el acceso será libre en red local?
