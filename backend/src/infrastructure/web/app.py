import os
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List

from src.infrastructure.settings.config import ConfigLoader
from src.infrastructure.settings.logger import get_logger
from src.interface_adapter.http_controllers.simulacion_controller import SimulacionController
from src.interface_adapter.repositories.dinamico_gateway import DinamicoParametrosGateway
from src.interface_adapter.presenter.json_presenter import JSONSimulacionPresenter

app = FastAPI(
    title="FITBA - API de Impacto Económico",
    description="API REST de simulación de OEE y punto de equilibrio financiero para la cooperativa Madygraf.",
    version="1.0.0"
)

# Permitir CORS para facilitar desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logger técnico
web_logger = get_logger("FITBA.Web")

# Esquemas de Validación Pydantic
class OEEBaseSchema(BaseModel):
    disponibilidad: float = Field(..., ge=0.0, le=1.0)
    rendimiento: float = Field(..., ge=0.0, le=1.0)
    calidad: float = Field(..., ge=0.0, le=1.0)

class InversionSchema(BaseModel):
    objetivo_anr: float = Field(..., gt=0)
    factor_ipc_acumulado: float = Field(..., ge=1.0)

class ProductoSchema(BaseModel):
    id: str
    nombre: str
    precio_unitario: float = Field(..., gt=0)
    costo_marginal_unitario: float = Field(..., ge=0)

class LineaProduccionSchema(BaseModel):
    id: str
    nombre: str
    capacidad_nominal: float = Field(..., gt=0)
    productos_compatibles: List[str]

class MixProduccionSchema(BaseModel):
    producto_id: str
    porcentaje: float = Field(..., ge=0.0, le=1.0)

class EscenarioDetalleSchema(BaseModel):
    nombre: str
    tasa_crecimiento_mensual: float = Field(..., ge=0.0, le=1.0)
    factor_demanda: float = Field(1.0, ge=0.0, le=2.0)

class SimularRequestSchema(BaseModel):
    inversion: InversionSchema
    oee: OEEBaseSchema
    productos: List[ProductoSchema]
    lineas_produccion: List[LineaProduccionSchema]
    mix_objetivo: List[MixProduccionSchema]
    escenarios: dict[str, EscenarioDetalleSchema]


@app.middleware("http")
async def add_correlation_id(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


@app.get("/api/config")
def get_config():
    """
    Retorna la configuración actual y el tiempo de inicio de la aplicación.
    """
    loader = ConfigLoader()
    return {
        "mode": loader.get_app_mode(),
        "start_time": loader.get_start_time()
    }


@app.get("/api/v1/simulacion/parametros")
def get_params():
    """
    Retorna los parámetros base procesados (a valor presente) según el contrato API.
    """
    try:
        loader = ConfigLoader()
        raw_data = loader._raw_data
        gateway = DinamicoParametrosGateway(raw_data)
        inversion = gateway.get_inversion()
        
        # Preparar serie IPC para frontend
        ipc_serie = []
        if "indices" in raw_data and "ipc" in raw_data["indices"]:
            serie = raw_data["indices"]["ipc"]["serie_mensual"]
            ipc_serie = [{"mes": k, "tasa": v} for k, v in serie.items()]
            
        return {
            "inversion": {
                "monto_anr": inversion.monto_anr,
                "monto_actualizado": inversion.monto_actualizado,
                "moneda": "ARS",
                "fecha_base": "2025-02-01",
                "fecha_objetivo": "2026-03-01"
            },
            "oee": {
                "disponibilidad": raw_data["oee"]["linea_base"]["disponibilidad"],
                "rendimiento": raw_data["oee"]["linea_base"]["rendimiento"],
                "calidad": raw_data["oee"]["linea_base"]["calidad"]
            },
            "productos": raw_data["productos"],
            "lineas_produccion": raw_data["lineas_produccion"],
            "mix_objetivo": {m["producto_id"]: m["porcentaje"] for m in raw_data["mix_objetivo"]},
            "ipc_serie": ipc_serie
        }
    except Exception as e:
        web_logger.error(f"Error cargando parámetros base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"No se pudieron cargar los parámetros: {str(e)}")


@app.post("/api/v1/simulacion/ejecutar")
def post_simular(payload: SimularRequestSchema, request: Request):
    """
    Ejecuta el controlador de simulación usando parámetros dinámicos y
    retorna los resultados formateados en JSON según el contrato API.
    """
    try:
        correlation_id = request.state.correlation_id
        web_logger.info(f"[{correlation_id}] Recibida petición de simulación dinámica...")
        raw_dict = payload.model_dump()
        
        # Inyección de dependencias bajo Clean Architecture
        gateway = DinamicoParametrosGateway(raw_dict)
        presenter = JSONSimulacionPresenter()
        sim_logger = get_logger("FITBA.SimulacionWeb")
        
        controller = SimulacionController(
            gateway=gateway,
            presenter=presenter,
            logger=sim_logger
        )
        
        # Ejecución
        controller.ejecutar_simulacion()
        
        return presenter.response_data
        
    except Exception as e:
        web_logger.error(f"Error durante la simulación: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error al procesar la simulación: {str(e)}")


# Servir Frontend Estático
# Determinamos la ruta absoluta al directorio static
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "frontend")

if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    web_logger.info(f"Directorio estático montado exitosamente en: {static_dir}")
else:
    web_logger.warning(f"El directorio estático {static_dir} no existe aún. Por favor créalo.")
