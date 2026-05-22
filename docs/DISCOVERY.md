# DISCOVERY - Dudas e Incertidumbres Pendientes

## Modelo de Negocio
1. **Mix de Ventas:** ¿Cómo se distribuye porcentualmente el mix de producción entre los diferentes tipos de productos? ¿Este mix es constante o varía con el volumen?
2. **Capacidad de Absorción:** ¿El mercado realmente garantiza la absorción del 100% de la producción incremental sin necesidad de stock?
3. **Costo Energético:** ¿Cuál es el coeficiente de consumo eléctrico marginal por cada unidad producida por encima de la línea base?
4. **Impacto en Turnos:** ¿A partir de qué volumen de producción el costo de "hora operativa" ($12.000) deja de ser fijo y requiere la contratación/apertura de nuevos turnos?

## Definiciones Técnicas
1. **Validación de IPC:** ¿El factor IPC debe aplicarse mensualmente sobre el flujo de caja o solo una vez sobre el monto objetivo de la inversión? (Actualmente se aplica sobre el objetivo).

## Integración de Interfaz Web (FastAPI + HTML + Bootstrap + JS)
1. **Persistencia de Parámetros Modificados:** Cuando un usuario edita los parámetros en el dashboard web y ejecuta la simulación, ¿los cambios deben guardarse permanentemente en el archivo del servidor (`data/params.json`), guardarse localmente en el navegador (`localStorage`) para que se mantengan en su navegador en futuras sesiones, o ser estrictamente volátiles (en memoria únicamente para esa petición)?
2. **Bibliotecas de Visualización Permitidas:** Para lograr una experiencia premium con gráficos dinámicos interactivos del flujo de caja acumulado y la curva de disponibilidad de OEE, ¿está permitido usar Chart.js (u otra alternativa como ApexCharts o Plotly) a través de una red de distribución de contenido (CDN)?
3. **Mecanismo de Ejecución y Puerto:** ¿El servidor web de FastAPI se iniciará como un comando separado (ej. `python3 main.py --web` o `uvicorn src.infrastructure.web.app:app --reload`), o se integrará en el punto de entrada existente? ¿Qué puerto por defecto (ej. 8000, 5000) es el preferido?
4. **Vista de Auditoría Detallada (Modo Debug):** En la CLI, el flag `--debug` expone la traza técnica mes a mes. En la interfaz web, ¿queremos ofrecer una vista de "Detalle de Auditoría" (como una tabla expandible con el desglose mensual para cada escenario o un modal detallado) o es suficiente mostrar la tabla resumida de meses de repago?
5. **Seguridad y Control de Acceso:** Dado que las simulaciones manejan datos financieros del ANR y costos de producción de la planta de la cooperativa Madygraf, ¿se requiere algún tipo de login/autenticación básica para acceder al panel, o debe ser de acceso público abierto dentro de la red local?

