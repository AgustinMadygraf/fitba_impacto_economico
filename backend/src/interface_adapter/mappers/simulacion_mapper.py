"""
Path: backend/src/interface_adapter/mappers/simulacion_mapper.py
"""

from src.interface_adapter.schemas import SimularRequestSchema

class SimulacionMapper:
    @staticmethod
    def map_request_to_dict(payload: SimularRequestSchema) -> dict:
        return {
            "inversion": {"objetivo_anr": payload.inversion.objetivo_anr, "fecha_base": payload.inversion.fecha_base},
            "oee_base": payload.oee_base.model_dump(),
            "catalogo": {
                "productos": [p.model_dump() for p in payload.catalogo.productos],
                "lineas": [l.model_dump() for l in payload.catalogo.lineas]
            },
            "mix_objetivo": [m.model_dump() for m in payload.mix_objetivo],
            "escenarios": {k: v.model_dump() for k, v in payload.escenarios.items()},
            "capacidad_instalada": payload.capacidad_instalada.model_dump(),
            "ipc_override": payload.ipc
        }
