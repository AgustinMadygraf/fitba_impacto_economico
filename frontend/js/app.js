/**
 * Path: src/infrastructure/web/static/js/app.js
 */

import { SimulationController } from './simulationController.js';
import { FormBinder } from './formBinder.js';
import { UIUpdater } from './uiUpdater.js';

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
  const canvasElement = document.getElementById('chart-proyeccion');
  const ctx = canvasElement ? canvasElement.getContext('2d') : null;
  let myChart = null;

  fetch('/api/v1/simulacion/parametros')
    .then(res => res.json())
    .then(async data => {
      poblarFormulario(data);
      if (loading) loading.classList.remove('d-none');
      try {
        const formData = FormBinder.getSimulationData();
        const results = await SimulationController.runSimulation(formData);
        actualizarUI(results);
      } catch (error) {
        if (getMode() === 'development') console.error('Error en simulación automática:', {error});
      } finally {
        if (loading) loading.classList.add('d-none');
      }
    })
    .catch(err => { if (getMode() === 'development') console.error('Error cargando parámetros:', {err}) });

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (loading) loading.classList.remove('d-none');
    
    try {
      const formData = FormBinder.getSimulationData();
      const results = await SimulationController.runSimulation(formData);
      actualizarUI(results);
    } catch (error) {
      console.error('[FITBA] Error crítico en simulación:', error);
      alert('Error en simulación: ' + error.message);
    } finally {
      if (loading) loading.classList.add('d-none');
    }
  });

  function renderProductoRow(producto) {
    const container = document.getElementById("lista-productos");
    if (!container) return;
    const div = document.createElement("div");
    div.className = "card mb-2 p-2 border-0 bg-dark bg-opacity-10 item-producto";
    div.dataset.id = producto.id;
    div.innerHTML = `
      <input type="text" class="form-control mb-1 input-producto-nombre" value="${producto.nombre}" placeholder="Nombre">
      <div class="d-flex gap-2">
        <input type="number" step="0.1" class="form-control input-producto-precio" value="${producto.precio_unitario}" placeholder="Precio">
        <input type="number" step="0.1" class="form-control input-producto-costo" value="${producto.costo_marginal_unitario}" placeholder="Costo">
      </div>
    `;
    container.appendChild(div);
  }

  function renderLineaRow(linea) {
    const container = document.getElementById("lista-lineas");
    if (!container) return;
    const div = document.createElement("div");
    div.className = "card mb-2 p-2 border-0 bg-dark bg-opacity-10 item-linea";
    div.dataset.id = linea.id;
    div.innerHTML = `
      <input type="text" class="form-control mb-1 input-linea-nombre" value="${linea.nombre}" placeholder="Nombre">
      <input type="number" step="1000" class="form-control input-linea-capacidad" value="${linea.capacidad_nominal}" placeholder="Capacidad Nominal">
    `;
    container.appendChild(div);
  }

  function poblarFormulario(data) {
    if (!data.inversion || !data.productos || !data.lineas_produccion) {
        console.error("Error: Contrato API violado, faltan campos en la respuesta", data);
        return;
    }

    const inputAnr = document.getElementById('input-anr');
    if (inputAnr) inputAnr.value = data.inversion.monto_actualizado;
    
    const listaProductos = document.getElementById("lista-productos");
    const listaLineas = document.getElementById("lista-lineas");
    const listaIpc = document.getElementById("lista-ipc");

    if (listaProductos) listaProductos.innerHTML = "";
    if (listaLineas) listaLineas.innerHTML = "";
    if (listaIpc) listaIpc.innerHTML = "";

    data.productos.forEach(p => renderProductoRow(p));
    data.lineas_produccion.forEach(l => renderLineaRow(l));
    
    if (listaIpc && data.ipc_serie) {
       listaIpc.innerHTML = data.ipc_serie.map(item => `
         <div>Mes ${item.mes}: ${(item.tasa * 100).toFixed(1)}%</div>
       `).join('');
    } else {
       console.warn("[FITBA] lista-ipc no encontrado en el DOM o sin datos");
    }
  }

  function actualizarUI(results) {
    UIUpdater.actualizarKPIs(results);
    UIUpdater.renderizarTabla(results.resultados);
    if (ctx) renderizarGrafico(results.proyecciones, results.target_repago);
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
