"""
Path: main.py
"""

from src.infrastructure.settings.config import ConfigLoader
from src.entities.escenario import Escenario
from src.use_cases.simular_impacto import SimularImpactoEconomico

def run():
    # 1. Carga de Configuración (Delegada a Infraestructura)
    config = ConfigLoader()
    
    inversion = config.get_inversion()
    producto = config.get_producto()
    oee_base = config.get_oee_base()
    produccion = config.get_produccion_base()
    capacidad = config.get_capacidad_instalada()
    
    print("-" * 60)
    print(f"SIMULACIÓN DE IMPACTO ECONÓMICO - FITBA (Configuración Delegada)")
    print(f"Target de Repago Actualizado: ${inversion.monto_actualizado:,.2f}")
    print(f"OEE Línea Base: {oee_base.valor*100:.2f}%")
    print(f"Nota: Se asume absorción del 100% de la producción (Push Model).")
    print("-" * 60)
    print(f"{'ESCENARIO':<15} | {'CRECIMIENTO':<12} | {'REPAGO (MESES)':<15}")
    print("-" * 60)
    
    # 2. Ejecución de Escenarios
    escenarios_data = config.get_escenarios_raw()
    
    for clave, datos in escenarios_data.items():
        escenario = Escenario(
            nombre=datos['nombre'],
            tasa_crecimiento=datos['tasa_crecimiento_mensual'],
            factor_demanda=1.0  # Mantenemos 100% de absorción según definición industrial
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

    print("-" * 60)

if __name__ == "__main__":
    run()
