import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, List

from src.infrastructure.settings.config import ConfigLoader
from src.infrastructure.settings.logger import get_logger
from src.interface_adapter.controller.simulacion_controller import SimulacionController
from src.interface_adapter.gateway.dinamico_gateway import DinamicoParametrosGateway
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
web_logger = get_logger("FITBA.Web", debug=True)

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
    oee: dict[str, Any]
    productos: List[ProductoSchema]
    lineas_produccion: List[LineaProduccionSchema]
    mix_objetivo: List[MixProduccionSchema]
    escenarios: dict[str, EscenarioDetalleSchema]


@app.get("/api/config")
def get_config():
    """
    Retorna la configuración actual de la aplicación.
    """
    loader = ConfigLoader()
    return {"mode": loader.get_app_mode()}


@app.get("/api/params")
def get_params():
    """
    Retorna los parámetros base cargados desde data/params.json.
    """
    try:
        loader = ConfigLoader()
        return loader._raw_data
    except Exception as e:
        web_logger.error(f"Error cargando parámetros base: {str(e)}")
        raise HTTPException(status_code=500, detail=f"No se pudieron cargar los parámetros: {str(e)}")


@app.post("/api/simular")
def post_simular(payload: SimularRequestSchema):
    """
    Ejecuta el controlador de simulación usando parámetros dinámicos y
    retorna los resultados formateados en JSON a través de un Presenter especializado.
    """
    try:
        web_logger.info("Recibida petición de simulación dinámica...")
        raw_dict = payload.model_dump()
        
        # Inyección de dependencias bajo Clean Architecture
        gateway = DinamicoParametrosGateway(raw_dict)
        presenter = JSONSimulacionPresenter()
        sim_logger = get_logger("FITBA.SimulacionWeb", debug=True)
        
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
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    web_logger.info(f"Directorio estático montado exitosamente en: {static_dir}")
else:
    web_logger.warning(f"El directorio estático {static_dir} no existe aún. Por favor créalo.")
