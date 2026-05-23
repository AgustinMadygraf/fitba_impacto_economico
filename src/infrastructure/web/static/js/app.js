/**
 * Path: src/infrastructure/web/static/js/app.js
 */

import { SimulationController } from './simulationController.js';

/**
 * Inicializador de la aplicación.
 */
document.addEventListener('DOMContentLoaded', async () => {
  try {
    if (window.CONFIG_LOADED) await window.CONFIG_LOADED;
  } catch (e) {
    console.warn("Configuración no cargada, usando modo producción por defecto.");
  }
  
  const getMode = () => (window.APP_CONFIG && window.APP_CONFIG.mode) || 'production';

  const form = document.getElementById('form-simulacion');
  const loading = document.getElementById('loading');
  const ctx = document.getElementById('chart-proyeccion').getContext('2d');
  let myChart = null;

  fetch('/api/params')
    .then(res => res.json())
    .then(async data => {
      poblarFormulario(data);
      loading.classList.remove('d-none');
      try {
        const results = await SimulationController.runSimulation(getFormData());
        actualizarUI(results);
      } catch (error) {
        if (getMode() === 'development') console.error('Error en simulación automática:', {error});
      } finally {
        loading.classList.add('d-none');
      }
    })
    .catch(err => { if (getMode() === 'development') console.error('Error cargando parámetros:', {err}) });

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

/**
 * Recolecta los datos del formulario.
 * @returns {FormData} Los datos recolectados.
 */
  function getFormData() {
    return {
      anr: document.getElementById('input-anr').value,
      ipc: document.getElementById('input-ipc').value,
      dispBase: document.getElementById('input-disp-base').value,
      perf: document.getElementById('input-perf').value,
      quality: document.getElementById('input-quality').value,
      volBase: document.querySelector(".input-linea-capacidad").value,
      precio: document.getElementById('input-precio').value,
      costo: document.getElementById('input-costo').value,
      rateDesfavorable: document.getElementById('input-rate-desfavorable').value,
      rateProyectado: document.getElementById('input-rate-proyectado').value,
      rateFavorable: document.getElementById('input-rate-favorable').value,
    };
  }
  /**
   * Renderiza dinámicamente un producto en la UI.
   * @param {Object} producto - Datos del producto.
   */
  function renderProductoRow(producto = { nombre: "Producto A", precio: 0, costo: 0 }) {
    const container = document.getElementById("lista-productos");
    container.innerHTML = `
      <div class="card mb-2 p-2 border-0 bg-dark bg-opacity-10">
        <input type="text" class="form-control mb-1" value="${producto.nombre}" placeholder="Nombre">
        <div class="d-flex gap-2">
          <input type="number" step="0.1" class="form-control input-producto-precio" value="${producto.precio}" placeholder="Precio">
          <input type="number" step="0.1" class="form-control input-producto-costo" value="${producto.costo}" placeholder="Costo">
        </div>
      </div>
    `;
    document.getElementById("add-producto").disabled = true; // Alcance Inicial
  }
  /**
   * Renderiza dinámicamente una línea en la UI.
   * @param {Object} linea - Datos de la línea.
   */
  function renderLineaRow(linea = { nombre: "Linea 1", capacidad: 0 }) {
    const container = document.getElementById("lista-lineas");
    container.innerHTML = `
      <div class="card mb-2 p-2 border-0 bg-dark bg-opacity-10">
        <input type="text" class="form-control mb-1" value="${linea.nombre}" placeholder="Nombre">
        <input type="number" class="form-control input-linea-capacidad" value="${linea.capacidad}" placeholder="Capacidad">
      </div>
    `;
    document.getElementById("add-linea").disabled = true; // Alcance Inicial
  }

/**
 * Pobla el formulario con datos iniciales.
 * @param {Object} data - Datos iniciales.
 */
  function poblarFormulario(data) {
    document.getElementById('input-anr').value = data.inversion.objetivo_anr;
    document.getElementById('input-ipc').value = ((data.inversion.factor_ipc_acumulado - 1) * 100).toFixed(1);
    
    document.getElementById("input-quality").value = (data.oee.linea_base.calidad * 100).toFixed(1);
    document.getElementById('input-disp-base').value = (data.oee.linea_base.disponibilidad * 100).toFixed(1);
    document.getElementById('input-perf').value = (data.oee.linea_base.rendimiento * 100).toFixed(1);
    document.getElementById('input-precio').value = data.productos[0].precio_unitario;
    renderProductoRow({
        nombre: data.productos[0].nombre,
        precio: data.productos[0].precio_unitario,
        costo: data.productos[0].costo_marginal_unitario
    });
    
    renderLineaRow({
        nombre: data.lineas_produccion[0].nombre,
        capacidad: data.lineas_produccion[0].capacidad_nominal
    });
    document.getElementById('input-costo').value = data.productos[0].costo_marginal_unitario;
    
    document.getElementById('input-rate-desfavorable').value = (data.escenarios.desfavorable.tasa_crecimiento_mensual * 100).toFixed(1);
    document.getElementById('input-rate-proyectado').value = (data.escenarios.proyectado.tasa_crecimiento_mensual * 100).toFixed(1);
    document.getElementById('input-rate-favorable').value = (data.escenarios.favorable.tasa_crecimiento_mensual * 100).toFixed(1);
  }

/**
 * Actualiza la UI con los resultados.
 * @param {Object} results - Resultados de la simulación.
 */
  function actualizarUI(results) {
    document.getElementById('kpi-target-actualizado').textContent = '$' + results.target_repago.toLocaleString('es-AR', { minimumFractionDigits: 0 });
    document.getElementById('kpi-oee-base').textContent = (results.oee_base * 100).toFixed(2) + '%';
    
    const oeeMaxVal = 0.85 * (parseFloat(document.getElementById('input-perf').value)/100) * (parseFloat(document.getElementById('input-quality').value)/100);
    document.getElementById('kpi-oee-max').textContent = (oeeMaxVal * 100).toFixed(2) + '%';
    
    renderizarTabla(results.resultados);
    renderizarGrafico(results.proyecciones, results.target_repago);
  }

  function renderizarTabla(resultados) {
    const tbody = document.getElementById('resultados-tbody');
    tbody.innerHTML = '';
    resultados.forEach(res => {
      const mesText = res.mes_repago ? 'Mes ' + res.mes_repago : 'Límite >24m';
      const viableClass = res.viable ? 'badge-favorable' : 'badge-desfavorable';
      tbody.innerHTML += '<tr>' +
        '<td><span class="badge-escenario badge-' + res.escenario.toLowerCase() + '">' + res.escenario + '</span></td>' +
        '<td class="text-center">' + (res.tasa * 100).toFixed(1) + '%</td>' +
        '<td class="text-center fw-bold text-white">' + mesText + '</td>' +
        '<td class="text-center"><span class="badge-escenario ' + viableClass + '">' + (res.viable ? 'Viable' : 'No Viable') + '</span></td>' +
        '</tr>';
    });
  }

  function renderizarGrafico(proyecciones, target) {
    try {
      const labels = Array.from({ length: 24 }, (_, i) => 'Mes ' + (i + 1));
      const datasets = [
        { label: 'Favorable', data: proyecciones.favorable, borderColor: 'hsl(145, 80%, 45%)', borderWidth: 3, tension: 0.3, pointRadius: 0 },
        { label: 'Proyectado', data: proyecciones.proyectado, borderColor: 'hsl(195, 100%, 50%)', borderWidth: 3, tension: 0.3, pointRadius: 0 },
        { label: 'Desfavorable', data: proyecciones.desfavorable, borderColor: 'hsl(25, 95%, 50%)', borderWidth: 2, tension: 0.3, pointRadius: 0 },
        { label: 'Target Repago', data: Array(24).fill(target), borderColor: 'rgba(255, 99, 132, 0.6)', borderWidth: 2, borderDash: [5, 5], pointRadius: 0 }
      ];
      if (myChart) {
        myChart.data.datasets = datasets;
        myChart.update();
      } else {
        myChart = new Chart(ctx, {
          type: 'line',
          data: { labels, datasets },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#ccc' } } },
            scales: {
              x: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#888' } },
              y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#888', callback: function(v) { return '$' + (v / 1e6).toFixed(1) + 'M'; } } }
            }
          }
        });
      }
    } catch (error) {
      if (getMode() === 'development') console.error('Error renderizando gráfico', { error });
    }
  }
});
