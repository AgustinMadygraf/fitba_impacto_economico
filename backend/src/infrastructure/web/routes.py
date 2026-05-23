import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

from src.infrastructure.settings.config import ConfigLoader
from src.infrastructure.settings.logger import get_logger
from src.interface_adapter.controllers.simulacion_controller import SimulacionController
from src.interface_adapter.repositories.json_parametros_repository import JsonParametrosRepository
from src.interface_adapter.presenter.json_presenter import JSONSimulacionPresenter
from src.application.simular_impacto_economico_use_case import SimularImpactoEconomico

app = FastAPI(title="FITBA - API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
web_logger = get_logger("FITBA.Web")

class OEEBaseSchema(BaseModel):
    disponibilidad: float; rendimiento: float; calidad: float; limite_disponibilidad: float
class InversionSchema(BaseModel):
    objetivo_anr: float; fecha_base: str
class ProductoSchema(BaseModel):
    id: str; nombre: str; precio_unitario: float; costo_marginal_unitario: float
class LineaProduccionSchema(BaseModel):
    id: str; nombre: str; capacidad_nominal: float; productos_compatibles: List[str]
class CatalogoSchema(BaseModel):
    productos: List[ProductoSchema]
    lineas: List[LineaProduccionSchema]
class MixProduccionSchema(BaseModel):
    producto_id: str; porcentaje: float
class EscenarioDetalleSchema(BaseModel):
    nombre: str; tasa_crecimiento_mensual: float; factor_demanda: float
class SimularRequestSchema(BaseModel):
    inversion: InversionSchema
    oee_base: OEEBaseSchema
    catalogo: CatalogoSchema
    mix_objetivo: List[MixProduccionSchema]
    escenarios: Dict[str, EscenarioDetalleSchema]

@app.get("/api/config")
def get_config():
    loader = ConfigLoader()
    return {"mode": loader.get_app_mode(), "start_time": loader.get_start_time()}

@app.get("/api/v1/simulacion/parametros")
def get_params():
    try:
        loader = ConfigLoader()
        raw_data = loader._raw_data
        productos = [
            {"id": p["id"], "nombre": p["nombre"], "precio": p["precio"], "costo": p["costo"]}
            for p in raw_data["catalogo"]["productos"]
        ]
        return {
            "inversion": {"monto_anr": raw_data["inversion"]["objetivo_anr"], "monto_actualizado": raw_data["inversion"]["objetivo_anr"]},
            "oee": raw_data["oee_base"],
            "productos": productos,
            "lineas_produccion": raw_data["catalogo"]["lineas"],
            "ipc_serie": [{"mes": k, "tasa": v} for k, v in raw_data["ipc_serie"]["serie_mensual"].items()]
        }
    except Exception as e:
        web_logger.error(f"Error en GET /api/v1/simulacion/parametros: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/simulacion/ejecutar")
def post_simular(payload: SimularRequestSchema):
    try:
        raw_dict = {
            "inversion": {"objetivo_anr": payload.inversion.objetivo_anr, "fecha_base": payload.inversion.fecha_base},
            "oee_base": payload.oee_base.model_dump(),
            "catalogo": {
                "productos": [{"id": p.id, "nombre": p.nombre, "precio_unitario": p.precio_unitario, "costo_marginal_unitario": p.costo_marginal_unitario} for p in payload.catalogo.productos],
                "lineas": [l.model_dump() for l in payload.catalogo.lineas]
            },
            "mix_objetivo": [m.model_dump() for m in payload.mix_objetivo],
            "escenarios": {k: v.model_dump() for k, v in payload.escenarios.items()},
            "capacidad_instalada": {"capacidad_nominal_total_mensual": sum(l.capacidad_nominal for l in payload.catalogo.lineas)}
        }
        gateway = JsonParametrosRepository(raw_dict)
        presenter = JSONSimulacionPresenter()
        controller = SimulacionController(gateway, presenter, get_logger("FITBA.SimulacionSimulacion"))
        controller.ejecutar_simulacion()
        return presenter.response_data
    except Exception as e:
        web_logger.error(f"Error en POST /api/v1/simulacion/ejecutar: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "frontend")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
