from src.interface_adapter.presenter.json_presenter import JSONSimulacionPresenter

def test_presentar_resultados():
    presenter = JSONSimulacionPresenter()
    proyecciones = {'Escenario 1': [{'mes': 1, 'fecha': '03/2025', 'beneficio_acumulado': 100.0}]}
    resultados = [{'escenario': 'Escenario 1', 'tasa': 0.05, 'mes_repago': 12, 'viable': True}]
    
    presenter.presentar_resultados(target_repago=1000.0, oee_base=0.1, resultados=resultados, proyecciones=proyecciones)
    assert presenter.response_data["target_repago"] == 1000.0
    assert "proyecciones" in presenter.response_data
    assert "resultados" in presenter.response_data
