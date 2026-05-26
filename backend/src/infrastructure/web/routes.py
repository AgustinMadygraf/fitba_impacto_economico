"""
Path: backend/src/infrastructure/web/routes.py
"""

import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Dict, List, Optional

from src.infrastructure.settings.config import ConfigLoader
from src.infrastructure.settings.logger import get_logger
from src.interface_adapter.controllers.simulacion_controller import SimulacionController
from src.interface_adapter.presenter.json_presenter import JSONSimulacionPresenter
from src.interface_adapter.presenter.parametros_presenter import ParametrosPresenter
from src.domain.exceptions import FITBAError, ErrorValidacionDatos

app = FastAPI(title="FITBA - API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
web_logger = get_logger("FITBA.Web")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    web_logger.error(f"Error de Validación de Pydantic: {exc.errors()}")
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": exc.errors()})

@app.exception_handler(FITBAError)
async def fitba_exception_handler(request: Request, exc: FITBAError):
    status_code = status.HTTP_400_BAD_REQUEST if isinstance(exc, ErrorValidacionDatos) else status.HTTP_500_INTERNAL_SERVER_ERROR
    web_logger.error(f"Error de Negocio: {str(exc)}")
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})

class OEEBaseSchema(BaseModel):
    disponibilidad: float; rendimiento: float; calidad: float
class InversionSchema(BaseModel):
    objetivo_anr: float; fecha_base: str
class ProductoSchema(BaseModel):
    sku: str
    nombre: str
    precio_unitario: float
    ancho_bolsa: Optional[float] = 0.0
    alto_bolsa: Optional[float] = 0.0
    fuelle: Optional[float] = 0.0
    gramaje: Optional[float] = 0.0
    precio_bobina_kg: Optional[float] = 0.0
class LineaProduccionSchema(BaseModel):
    sku: str; nombre: str; capacidad_nominal: float; productos_compatibles: List[str]
class CapacidadInstaladaSchema(BaseModel):
    capacidad_nominal_por_hora: float; horas_por_turno: int; turnos_por_dia: int; dias_habiles_por_mes: int; dias_inhabiles_mensuales: int
class CatalogoSchema(BaseModel):
    productos: List[ProductoSchema]; lineas: List[LineaProduccionSchema]
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
    capacidad_instalada: CapacidadInstaladaSchema
    ipc: Optional[float] = None

@app.get("/api/config")
def get_config():
    loader = ConfigLoader()
    return {"mode": loader.get_app_mode(), "start_time": loader.get_start_time()}

@app.get("/api/v1/simulacion/parametros")
def get_params():
    loader = ConfigLoader()
    inversion = loader.get_inversion()
    presenter = ParametrosPresenter()
    return presenter.formatear(loader._raw_data, inversion)

@app.post("/api/v1/simulacion/ejecutar")
def post_simular(payload: SimularRequestSchema, request: Request):
    correlation_id = request.headers.get("X-Correlation-ID", "N/A")
    web_logger.info(f"[CID: {correlation_id}] POST /api/v1/simulacion/ejecutar iniciado")
    
    # Transformation logic is now hidden in the controller/gateway
    raw_dict = {
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
    
    # Minimal infrastructure setup
    presenter = JSONSimulacionPresenter()
    # Repository is created inside controller now
    controller = SimulacionController(None, presenter, get_logger(f"FITBA.Simulacion.{correlation_id}"))
    controller.ejecutar_simulacion_con_payload(raw_dict)
    
    web_logger.info(f"[CID: {correlation_id}] POST /api/v1/simulacion/ejecutar finalizado exitosamente")
    web_logger.info(f"Presenter response: {presenter.response_data.keys()}")
    return presenter.response_data

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "frontend")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
