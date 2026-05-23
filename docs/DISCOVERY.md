# DISCOVERY - Dudas e Incertidumbres Pendientes

## 1. Decisiones de Alcance (Fuera de Scope)
- **Gestión de Inventario Intermedio (Buffer):** Excluido del alcance.

## 2. Decisiones Arquitectónicas (Completadas)
- **Desacoplamiento de Entidades (Capacidad vs. OEE):** RESUELTO. La estructura de datos y el modelo de dominio se han desacoplado, tratando a la capacidad física y a la eficiencia operativa como entidades independientes.
- **Persistencia Orientada al Dominio (1:1):** RESUELTO. El archivo `params.json` ahora tiene una estructura plana donde cada entidad de dominio es un nodo independiente, eliminando jerarquías innecesarias.

## 3. Estado de la Deuda Técnica
1. **Repository Pattern Abstracto:** Pendiente. El repositorio actual conoce detalles de la implementación JSON.
2. **Mappers Dedicados:** Pendiente. La lógica de transformación entre capas está centralizada en los Repositorios/Adaptadores; se requiere mayor encapsulamiento mediante Mappers.
3. **Inyección de Dependencias:** Pendiente. Se requiere implementar un contenedor para inyectar repositorios y servicios en lugar de instanciación directa.

## 4. Próximos Pasos (En Desarrollo)
- **Modelo de Inflación (Ajuste Financiero):** Implementar la lógica de capitalización compuesta del ANR en el Caso de Uso, utilizando `IndiceFinanciero` para la proyección y cálculo de factores de ajuste mes a mes.
