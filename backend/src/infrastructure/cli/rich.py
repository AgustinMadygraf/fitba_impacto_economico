"""
Path: src/infrastructure/cli/rich.py
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from src.interface_adapter.presenter.simulacion_presenter import SimulacionPresenter

class RichSimulacionPresenter(SimulacionPresenter):
    """
    Implementación física del Presenter utilizando la librería rich para CLI.
    """
    
    def __init__(self):
        self.console = Console()

    def presentar_resultados(self, target_repago: float, oee_base: float, resultados: list):
        # 1. Panel de encabezado
        self.console.print(Panel(
            f"[bold blue]Target de Repago Actualizado:[/bold blue] [green]${target_repago:,.2f}[/green]\n"
            f"[bold blue]OEE Línea Base:[/bold blue] [yellow]{oee_base*100:.2f}%[/yellow]\n"
            f"[italic white]Nota: Se asume absorción del 100% de la producción (Push Model).[/italic white]",
            title="[bold white]SIMULACIÓN DE IMPACTO ECONÓMICO - FITBA[/bold white]",
            border_style="bright_blue"
        ))

        # 2. Tabla de resultados
        table = Table(
            title="[bold]Análisis de Repago por Escenario[/bold]",
            box=box.ROUNDED,
            header_style="bold cyan",
            show_footer=True
        )
        
        table.add_column("Escenario", style="bold", footer="Totales")
        table.add_column("Crecimiento (r)", justify="right")
        table.add_column("Repago (Meses)", justify="center", style="green")

        for res in resultados:
            mes_style = "green" if res['mes_repago'] else "red"
            resultado_str = f"{res['mes_repago']} meses" if res['mes_repago'] else "Fuera de horizonte"
            
            table.add_row(
                res['nombre'],
                f"{res['tasa']*100:.1f}%",
                f"[{mes_style}]{resultado_str}[/{mes_style}]"
            )

        self.console.print(table)
        self.console.print("\n")
