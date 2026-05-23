/**
 * Path: src/infrastructure/web/static/js/app.js
 */

import { SimulationController } from './simulationController.js';

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form-simulacion');
  const loading = document.getElementById('loading');

  // Inicialización: Cargar Parámetros
  fetch('/api/params')
    .then(res => res.json())
    .then(data => poblarFormulario(data))
    .catch(err => console.error('Error cargando parámetros:', err));

  // Manejador de Simulación
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    loading.classList.remove('d-none');
    
    try {
      const results = await SimulationController.runSimulation(getFormData());
      actualizarUI(results);
    } catch (error) {
      alert('Error en simulación: ' + error.message);
    } finally {
      loading.classList.add('d-none');
    }
  });

  // Funciones de Vista (Manipulación DOM)
  function getFormData() {
    return {
      anr: document.getElementById('input-anr').value,
      ipc: document.getElementById('input-ipc').value,
      dispBase: document.getElementById('input-disp-base').value,
      perf: document.getElementById('input-perf').value,
      quality: document.getElementById('input-quality').value,
      volBase: document.getElementById('input-vol-base').value,
      precio: document.getElementById('input-precio').value,
      costo: document.getElementById('input-costo').value,
      rateDesfavorable: document.getElementById('input-rate-desfavorable').value,
      rateProyectado: document.getElementById('input-rate-proyectado').value,
      rateFavorable: document.getElementById('input-rate-favorable').value,
    };
  }

  function poblarFormulario(data) {
    document.getElementById('input-anr').value = data.inversion.objetivo_anr;
    document.getElementById('input-ipc').value = ((data.inversion.factor_ipc_acumulado - 1) * 100).toFixed(1);
    document.getElementById('input-disp-base').value = (data.oee.linea_base.disponibilidad * 100).toFixed(1);
    document.getElementById('input-perf').value = (data.oee.linea_base.rendimiento * 100).toFixed(1);
    document.getElementById('input-quality').value = (data.oee.linea_base.calidad * 100).toFixed(1);
    document.getElementById('input-vol-base').value = data.produccion.volumen_mensual_base;
    document.getElementById('input-precio').value = data.produccion.precio_unitario_promedio;
    document.getElementById('input-costo').value = data.produccion.costos_variables.material_por_unidad;
    document.getElementById('input-rate-desfavorable').value = (data.escenarios.desfavorable.tasa_crecimiento_mensual * 100).toFixed(1);
    document.getElementById('input-rate-proyectado').value = (data.escenarios.proyectado.tasa_crecimiento_mensual * 100).toFixed(1);
    document.getElementById('input-rate-favorable').value = (data.escenarios.favorable.tasa_crecimiento_mensual * 100).toFixed(1);
  }

  function actualizarUI(results) {
    document.getElementById('kpi-target-actualizado').textContent = '$' + results.targetRepago.toLocaleString('es-AR', { minimumFractionDigits: 0 });
    document.getElementById('kpi-oee-base').textContent = (results.oeeBase * 100).toFixed(2) + '%';
    
    // Cálculo de capacidad máxima (Frontend UI concern)
    const oeeMaxVal = 0.85 * (parseFloat(document.getElementById('input-perf').value)/100) * (parseFloat(document.getElementById('input-quality').value)/100);
    document.getElementById('kpi-oee-max').textContent = (oeeMaxVal * 100).toFixed(2) + '%';
    
    renderizarTabla(results.resultados);
  }

  function renderizarTabla(resultados) {
    const tbody = document.getElementById('resultados-tbody');
    tbody.innerHTML = '';
    resultados.forEach(res => {
      const mesText = res.mes_repago ? 'Mes ' + res.mes_repago : 'Límite >24m';
      const viableClass = res.viable ? 'badge-favorable' : 'badge-desfavorable';
      const row = '<tr>' +
        '<td><span class="badge-escenario badge-' + res.escenario.toLowerCase() + '">' + res.escenario + '</span></td>' +
        '<td class="text-center">' + (res.tasa * 100).toFixed(1) + '%</td>' +
        '<td class="text-center fw-bold text-white">' + mesText + '</td>' +
        '<td class="text-center"><span class="badge-escenario ' + viableClass + '">' + (res.viable ? 'Viable' : 'No Viable') + '</span></td>' +
        '</tr>';
      tbody.innerHTML += row;
    });
  }
});
