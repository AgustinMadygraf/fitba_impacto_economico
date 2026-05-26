# Discovery - Refactorización de Capa de Datos

## Certezas
- agregar_meses en backend/src/application/ayudante_fechas.py es utilidad técnica y debe moverse a backend/src/infrastructure/utils/ayudante_fechas.py.
- CalculadorIPC en backend/src/application/calculador_ipc.py es lógica de negocio y debe moverse a backend/src/domain/services/calculador_ipc.py.

## Duda/Ambigüedad
- ¿Existen dependencias circulares potenciales al mover CalculadorIPC?
