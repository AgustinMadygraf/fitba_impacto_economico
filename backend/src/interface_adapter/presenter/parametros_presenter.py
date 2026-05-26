"""
Path: backend/src/interface_adapter/presenter/parametros_presenter.py
"""

from datetime import datetime
from src.domain.services.calculador_ipc import CalculadorIPC

class ParametrosPresenter:
    def formatear(self, raw_data, inversion) -> dict:
        
        # Lógica de cálculo de costo marginal movida de routes.py
        def calcular_costo(p):
            ancho_bobina = (p["ancho_bolsa"] * 2) + (p["fuelle"] * 2) + 4
            longitud_corte = p["alto_bolsa"] + (p["fuelle"] / 2) + 2
            superficie_m2 = (ancho_bobina * longitud_corte) / 10000
            peso_gr = superficie_m2 * p["gramaje"]
            return (peso_gr / 1000) * p["precio_bobina_kg"]

        productos = [
            {
                "sku": p["sku"], "nombre": p["nombre"], "precio_unitario": p["precio_unitario"], 
                "costo_marginal_unitario": calcular_costo(p)
            }
            for p in raw_data["catalogo"]["productos"]
        ]
        
        ipc_acumulado = 1.0
        if inversion.indice_base:
            ipc_acumulado = CalculadorIPC.calculate_factor(inversion.indice_base, inversion.fecha_base, datetime.now())

        ipc_serie_flat = [{"mes": f"{year}-{month}", "tasa": rate} for year, months in raw_data.get("ipc_serie", {}).get("datos", {}).items() for month, rate in months.items()]

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
