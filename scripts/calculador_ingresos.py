import sys
import os
import json

# Ajustar PYTHONPATH para importar desde backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from src.domain.services.calculador_ingresos import CalculadorIngresos
from src.interface_adapter.repositories.json_parametros_repository import JsonParametrosRepository

def calcular_desde_cli():
    # Cargar los datos desde el archivo json
    data_path = "backend/data/params.json"
    with open(data_path, 'r') as f:
        raw_data = json.load(f)
    
    # Inicializar repositorio con los datos cargados
    repo = JsonParametrosRepository(raw_data)
    
    # Obtener datos reales
    productos_list = repo.get_productos()
    productos = {p.sku: p for p in productos_list}
    mix = repo.get_mix_produccion()
    
    # Valores de ejemplo
    volumen_ventas = 1000.0
    volumen_produccion = 1000.0
    
    beneficio, ingresos, costos = CalculadorIngresos.calcular_beneficio_mensual(
        productos, mix, volumen_produccion, volumen_ventas
    )
    
    print(f"--- Informe de Ingresos Mensuales (Datos Reales) ---")
    print(f"Volumen de Ventas: {volumen_ventas}")
    print(f"Ingresos Totales: {ingresos}")
    print(f"Costos Totales: {costos}")
    print(f"Beneficio: {beneficio}")

if __name__ == "__main__":
    try:
        calcular_desde_cli()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
