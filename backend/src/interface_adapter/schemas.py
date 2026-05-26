"""
Path: backend/src/interface_adapter/schemas.py
"""

from pydantic import BaseModel
from typing import Dict, List, Optional

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
