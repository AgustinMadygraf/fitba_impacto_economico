from src.interface_adapter.presenter.json_presenter import JSONSimulacionPresenter

def test_presentar_resultados():
    presenter = JSONSimulacionPresenter()
    proyecciones = {'Escenario 1': [{'mes': 1, 'fecha': '03/2025', 'beneficio_acumulado': 100.0}]}
    
    presenter.presentar_resultados(mes_repago=12, proyecciones=proyecciones)
    assert presenter.response_data["mes_repago"] == 12
    assert "proyecciones" in presenter.response_data
