# DISCOVERY - Dudas e Incertidumbres Pendientes

## 1. Decisiones Confirmadas (Cerradas)
- **Stack Tecnológico:** Uso de **Chart.js** vía CDN para visualización y **FastAPI** para el backend.
- **Estrategia de Testing:** Framework **pytest** con estructura de carpetas por capas (unit/integration) y cobertura mínima del 80%.
- **Infraestructura CI:** Uso de hooks de git locales (`pre-push.sh`) como primera barrera de calidad.
- **Lógica de IPC:** El ajuste por inflación se aplica sobre el monto objetivo (Target) inicial, no sobre los flujos mensuales.

## 2. Modelo de Negocio (Pendientes)
1. **Mix de Ventas:** ¿Cómo se distribuye el mix de producción? ¿Es constante o varía con el volumen?
2. **Capacidad de Absorción:** ¿Se garantiza la venta del 100% incremental (Factor Demanda)?
3. **Costos de Escalamiento:** ¿A partir de qué volumen el costo de hora operativa (2.000) requiere la apertura de nuevos turnos?
5. **Estandarización de Impresoras:** ¿La "Impresora de Bolsas" dedicada tiene la misma velocidad/capacidad que la "Impresora en línea"?
6. **Gestión de Inventario Intermedio (Buffer):** ¿Existe stock intermedio entre máquinas dependientes o el sistema se detiene si una máquina falla (flujo puro)?

## 3. Interfaz Web de Tres Secciones
1. **Reactividad vs. Botón:** ¿La actualización de las secciones "Datos Intermedios" y "Salidas" debe ser automática al cambiar un input (Debounce) o requiere pulsar "Ejecutar Simulación"?
2. **Profundidad de Datos Intermedios:** ¿La Sección 2 debe incluir una tabla con el desglose mensual (traza de auditoría) o solo los KPI consolidados?
3. **Persistencia de Parámetros:** ¿Los ajustes realizados por el usuario en la "Sección de Entradas" deben persistir en `localStorage` para futuras sesiones o ser volátiles?
4. **Seguridad de Acceso:** Dado el carácter sensible de los costos de la cooperativa, ¿se requiere autenticación básica o el acceso será libre en red local?