"""
Punto de entrada principal para la simulación de impacto económico FITBA.
"""

from src.infrastructure.settings.config import ConfigLoader
from src.infrastructure.settings.logger import get_logger
from src.infrastructure.cli.rich import RichReporter
from src.entities.escenario import Escenario
from src.use_cases.simular_impacto import SimularImpactoEconomico

# Inicialización del logger estilo FastAPI para eventos del sistema
logger = get_logger()

def run():
    # 1. Inicialización de Infraestructura
    config = ConfigLoader()
    reporter = RichReporter()
    
    # 2. Carga de Datos de Dominio
    inversion = config.get_inversion()
    producto = config.get_producto()
    oee_base = config.get_oee_base()
    produccion = config.get_produccion_base()
    capacidad = config.get_capacidad_instalada()
    
    logger.info("Iniciando proceso de simulación FITBA...")
    
    # 3. Ejecución de Escenarios y Recolección de Resultados
    escenarios_data = config.get_escenarios_raw()
    resultados = []
    
    for clave, datos in escenarios_data.items():
        escenario = Escenario(
            nombre=datos['nombre'],
            tasa_crecimiento=datos['tasa_crecimiento_mensual'],
            factor_demanda=1.0 
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
        
        resultados.append({
            'nombre': escenario.nombre,
            'tasa': escenario.tasa_crecimiento,
            'mes_repago': mes_repago
        })

    # 4. Reporte Visual (Rich)
    reporter.report_simulation(
        target_repago=inversion.monto_actualizado,
        oee_base=oee_base.valor,
        resultados=resultados
    )
    
    logger.info("Simulación finalizada exitosamente.")

if __name__ == "__main__":
    run()
