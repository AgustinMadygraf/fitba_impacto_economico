"""
Path: backend/src/infrastructure/web/routes.py
"""

import os
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from src.infrastructure.settings.config import ConfigLoader
from src.infrastructure.settings.logger import get_logger
from src.interface_adapter.controllers.simulacion_controller import SimulacionController
from src.interface_adapter.repositories.json_parametros_repository import JsonParametrosRepository
from src.interface_adapter.presenter.json_presenter import JSONSimulacionPresenter
from src.application.simular_impacto_economico_caso_uso import CasoUsoSimularImpactoEconomico
from src.domain.services.calculador_ipc import CalculadorIPC
from src.domain.exceptions import FITBAError, ErrorValidacionDatos, ErrorCalculoFinanciero

app = FastAPI(title="FITBA - API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
web_logger = get_logger("FITBA.Web")

# Manejador de excepciones de validación (422)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    web_logger.error(f"Error de Validación de Pydantic: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

# Manejador de excepciones centralizado
@app.exception_handler(FITBAError)
async def fitba_exception_handler(request: Request, exc: FITBAError):
    status_code = status.HTTP_400_BAD_REQUEST if isinstance(exc, ErrorValidacionDatos) else status.HTTP_500_INTERNAL_SERVER_ERROR
    web_logger.error(f"Error de Negocio: {str(exc)}")
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )

class OEEBaseSchema(BaseModel):
    disponibilidad: float; rendimiento: float; calidad: float
class InversionSchema(BaseModel):
    objetivo_anr: float; fecha_base: str
class ProductoSchema(BaseModel):
    sku: str; nombre: str; precio_unitario: float; costo_marginal_unitario: float
class LineaProduccionSchema(BaseModel):
    sku: str; nombre: str; capacidad_nominal: float; productos_compatibles: List[str]
class CapacidadInstaladaSchema(BaseModel):
    capacidad_nominal_por_hora: float
    horas_por_turno: int
    turnos_por_dia: int
    dias_habiles_por_mes: int
    dias_inhabiles_mensuales: int
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
    capacidad_instalada: CapacidadInstaladaSchema
    ipc: Optional[float] = None

@app.get("/api/config")
def get_config():
    loader = ConfigLoader()
    return {"mode": loader.get_app_mode(), "start_time": loader.get_start_time()}

@app.get("/api/v1/simulacion/parametros")
def get_params():
    loader = ConfigLoader()
    raw_data = loader._raw_data
    inversion = loader.get_inversion()
    productos = [
        {"sku": p["sku"], "nombre": p["nombre"], "precio_unitario": p["precio_unitario"], "costo_marginal_unitario": p["costo_marginal_unitario"]}
        for p in raw_data["catalogo"]["productos"]
    ]
    
    ipc_acumulado = 1.0
    if inversion.indice_base:
        ipc_acumulado = CalculadorIPC.calculate_factor(inversion.indice_base, inversion.fecha_base, datetime.now())

    ipc_serie_flat = []
    ipc_data = raw_data.get("ipc_serie", {})
    for year, months in ipc_data.get("datos", {}).items():
        for month, rate in months.items():
            ipc_serie_flat.append({"mes": f"{year}-{month}", "tasa": rate})

    return {
        "inversion": {
            "monto_anr_nominal": raw_data["inversion"]["objetivo_anr"], 
            "monto_anr_real": round(raw_data["inversion"]["objetivo_anr"] * ipc_acumulado, 2),
            "fecha_base": raw_data["inversion"]["fecha_base"],
            "ipc_acumulado": ipc_acumulado
        },
        "oee": raw_data["oee_base"],
        "productos": productos,
        "lineas_produccion": raw_data["catalogo"]["lineas"],
        "capacidad_instalada": raw_data["capacidad_instalada"],
        "ipc_serie": ipc_serie_flat,
        "tasa_proyectada": raw_data.get("ipc_serie", {}).get("tasa_proyectada", 0.02)
    }

@app.post("/api/v1/simulacion/ejecutar")
def post_simular(payload: SimularRequestSchema, request: Request):
    correlation_id = request.headers.get("X-Correlation-ID", "N/A")
    web_logger.info(f"[CID: {correlation_id}] POST /api/v1/simulacion/ejecutar iniciado")
    
    raw_dict = {
        "inversion": {"objetivo_anr": payload.inversion.objetivo_anr, "fecha_base": payload.inversion.fecha_base},
        "oee_base": payload.oee_base.model_dump(),
        "catalogo": {
            "productos": [{"sku": p.sku, "nombre": p.nombre, "precio_unitario": p.precio_unitario, "costo_marginal_unitario": p.costo_marginal_unitario} for p in payload.catalogo.productos],
            "lineas": [l.model_dump() for l in payload.catalogo.lineas]
        },
        "mix_objetivo": [m.model_dump() for m in payload.mix_objetivo],
        "escenarios": {k: v.model_dump() for k, v in payload.escenarios.items()},
        "capacidad_instalada": payload.capacidad_instalada.model_dump(),
        "ipc_override": payload.ipc
    }
    gateway = JsonParametrosRepository(raw_dict)
    presenter = JSONSimulacionPresenter()
    controller = SimulacionController(gateway, presenter, get_logger(f"FITBA.Simulacion.{correlation_id}"))
    controller.ejecutar_simulacion()
    web_logger.info(f"[CID: {correlation_id}] POST /api/v1/simulacion/ejecutar finalizado exitosamente")
    return presenter.response_data

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "frontend")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
