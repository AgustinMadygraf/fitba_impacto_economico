from src.interface_adapter.presenter.json_presenter import JSONSimulacionPresenter

def test_presentar_resultados():
    presenter = JSONSimulacionPresenter()
    resultados = [
        {'nombre': 'Escenario 1', 'tasa': 0.05, 'mes_repago': 12},
        {'nombre': 'Escenario 2', 'tasa': 0.02, 'mes_repago': None}
    ]
    
    presenter.presentar_resultados(
        target_repago=1000.0,
        oee_base=0.1,
        resultados=resultados
    )
    
    assert presenter.response_data['exito'] is True
    assert presenter.response_data['target_repago'] == 1000.0
    assert len(presenter.response_data['resultados']) == 2
    assert presenter.response_data['resultados'][0]['viable'] is True
    assert presenter.response_data['resultados'][1]['viable'] is False
