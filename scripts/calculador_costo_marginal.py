import sys
import os
import json

# Ajustar PYTHONPATH para importar desde backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from src.interface_adapter.repositories.json_parametros_repository import JsonParametrosRepository

def auditar_costo_marginal():
    # Cargar los datos desde el archivo json
    data_path = "backend/data/params.json"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} no encontrado.")
        return

    with open(data_path, 'r') as f:
        raw_data = json.load(f)
    
    # Inicializar repositorio
    repo = JsonParametrosRepository(raw_data)
    productos = repo.get_productos()
    
    print(f"--- Auditoría de Cálculo de Costo Marginal ---")
    for p in productos:
        print(f"Producto: {p.nombre} (SKU: {p.sku})")
        print(f"  - Especificaciones: Ancho {p.ancho_bolsa}cm, Alto {p.alto_bolsa}cm, Fuelle {p.fuelle}cm")
        print(f"  - Insumos: Gramaje {p.gramaje} gr/m2, Precio Bobina ${p.precio_bobina_kg}/kg")
        
        # El cálculo es dinámico en la propiedad @property de la entidad Producto
        costo = p.costo_marginal_unitario
        
        print(f"  - Costo Marginal Calculado: ${costo:.4f}")
        print("-" * 40)

if __name__ == "__main__":
    try:
        auditar_costo_marginal()
    except Exception as e:
        print(f"Error en auditoría: {e}")
        sys.exit(1)
