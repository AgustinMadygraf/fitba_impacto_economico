"""
Path: backend/src/infrastructure/web/routes.py
"""

import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from src.infrastructure.settings.config import ConfigLoader
from src.infrastructure.settings.logger import get_logger
from src.interface_adapter.controllers.simulacion_controller import SimulacionController
from src.interface_adapter.presenter.json_presenter import JSONSimulacionPresenter
from src.interface_adapter.presenter.parametros_presenter import ParametrosPresenter
from src.interface_adapter.schemas import SimularRequestSchema
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
    
    # DI in routes for controller setup
    presenter = JSONSimulacionPresenter()
    # In a real app, inject gateway and logger via Depends, keeping it simple for now as requested
    controller = SimulacionController(None, presenter, get_logger(f"FITBA.Simulacion.{correlation_id}"))
    controller.ejecutar_simulacion_con_request(payload)
    
    web_logger.info(f"[CID: {correlation_id}] POST /api/v1/simulacion/ejecutar finalizado exitosamente")
    return presenter.response_data

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "frontend-legacy")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
