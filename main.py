import json
from src.entities.inversion import Inversion
from src.entities.producto import Producto
from src.entities.oee import OEE
from src.entities.produccion import Produccion
from src.entities.escenario import Escenario
from src.entities.capacidad_instalada import CapacidadInstalada
from src.use_cases.simular_impacto import SimularImpactoEconomico

def cargar_parametros(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def run():
    params = cargar_parametros('data/params.json')
    
    # 1. Instanciación de Entidades Base
    inversion = Inversion(
        monto_anr=params['inversion']['objetivo_anr'],
        factor_ipc=params['inversion']['factor_ipc_acumulado']
    )
    
    producto = Producto(
        nombre="Producto Genérico Madygraf",
        precio_unitario=params['produccion']['precio_unitario_promedio'],
        costos_marginales_unitarios=params['produccion']['costos_variables']['material_por_unidad']
    )
    
    oee_base = OEE(
        disponibilidad=params['oee']['linea_base']['disponibilidad'],
        rendimiento=params['oee']['linea_base']['rendimiento'],
        calidad=params['oee']['linea_base']['calidad']
    )
    
    # Produccion requiere un vector (según su dataclass), enviamos el base
    produccion = Produccion(
        volumen_base=params['produccion']['volumen_mensual_base'],
        volumen_vector=[params['produccion']['volumen_mensual_base']]
    )
    
    capacidad = CapacidadInstalada(
        limite_disponibilidad=params['oee']['limite_disponibilidad']
    )
    
    print("-" * 50)
    print(f"SIMULACIÓN DE IMPACTO ECONÓMICO - FITBA")
    print(f"Target de Repago Actualizado: ${inversion.monto_actualizado:,.2f}")
    print(f"OEE Línea Base: {oee_base.valor*100:.2f}%")
    print("-" * 50)
    print(f"{'ESCENARIO':<15} | {'CRECIMIENTO':<12} | {'REPAGO (MESES)':<15}")
    print("-" * 50)
    
    # 2. Ejecución por Escenario
    for clave, datos in params['escenarios'].items():
        escenario = Escenario(
            nombre=datos['nombre'],
            tasa_crecimiento=datos['tasa_crecimiento_mensual'],
            factor_demanda=datos['factor_demanda']
        )
        
        simulador = SimularImpactoEconomico(
            inversion=inversion,
            producto=producto,
            oee_base=oee_base,
            produccion=produccion,
            escenario=escenario,
            capacidad=capacidad
        )
        
        mes_repago = simulador.ejecutar()
        
        resultado = f"{mes_repago} meses" if mes_repago else "Fuera de horizonte"
        print(f"{escenario.nombre:<15} | {escenario.tasa_crecimiento*100:>10.1f}% | {resultado:<15}")

    print("-" * 50)

if __name__ == "__main__":
    run()
