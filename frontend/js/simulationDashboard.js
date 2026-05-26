/**
 * Path: src/infrastructure/web/static/js/simulationDashboard.js
 */

import { SimulationController } from './simulationController.js';
import { SimulationFormBinder } from './simulationFormBinder.js';
import { SimulationUIUpdater } from './simulationUIUpdater.js';
import { UINotifier } from './uiNotifier.js';

document.addEventListener('DOMContentLoaded', async () => {
  const form = document.getElementById('form-simulacion');
  const loading = document.getElementById('loading');
  const canvasElement = document.getElementById('chart-proyeccion');
  const ctx = canvasElement ? canvasElement.getContext('2d') : null;
  let realAnr = 0;

  // console.log('[FITBA] Dashboard: Cargando parámetros iniciales');
  fetch('/api/v1/simulacion/parametros')
    .then(res => res.json())
    .then(async data => {
      // console.log('[FITBA] Dashboard: Parámetros cargados', data);
      realAnr = data.inversion.monto_anr_real;
      poblarFormulario(data);
      if (loading) loading.classList.remove('d-none');
      try {
        const formData = SimulationFormBinder.getSimulationData();
        const results = await SimulationController.runSimulation(formData);
        actualizarUI(results, realAnr);
      } catch (error) {
        console.error("[FITBA ERROR] Simulation failed:", error);
      } finally {
        if (loading) loading.classList.add('d-none');
      }
    })
    .catch(error => {
      console.error('[FITBA] Dashboard: Error cargando parámetros', error);
      UINotifier.showError('Error cargando configuración inicial');
    });

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    // console.log('[FITBA] Dashboard: Form submit');
    if (loading) loading.classList.remove('d-none');
    try {
      const formData = SimulationFormBinder.getSimulationData();
      const results = await SimulationController.runSimulation(formData);
      actualizarUI(results, realAnr);
    } catch (error) {
      console.error("[FITBA ERROR] Submit simulation failed:", error);
    } finally {
      if (loading) loading.classList.add('d-none');
    }
  });

  function renderProductoRow(producto) {
    const container = document.getElementById("lista-productos");
    if (!container) return;
    const div = document.createElement("div");
    div.className = "card mb-2 p-2 border-0 bg-dark bg-opacity-10 item-producto";
    div.dataset.sku = producto.sku;
    div.innerHTML = `
      <input type="text" class="form-control mb-1 input-producto-nombre" value="${producto.nombre}" placeholder="Nombre">
      <div class="d-flex gap-2">
        <input type="number" step="0.1" class="form-control input-producto-precio" value="${producto.precio || 0}" placeholder="Precio">
        <input type="number" step="0.1" class="form-control input-producto-costo" value="${producto.costo || 0}" placeholder="Costo">
      </div>
    `;
    container.appendChild(div);
  }

  function renderLineaRow(linea) {
    const container = document.getElementById("lista-lineas");
    if (!container) return;
    const div = document.createElement("div");
    div.className = "card mb-2 p-2 border-0 bg-dark bg-opacity-10 item-linea";
    div.dataset.sku = linea.sku;
    div.innerHTML = `
      <input type="text" class="form-control mb-1 input-linea-nombre" value="${linea.nombre}" placeholder="Nombre">
      <input type="number" step="1000" class="form-control input-linea-capacidad" value="${linea.capacidad_nominal || 0}" placeholder="Capacidad Nominal">
    `;
    container.appendChild(div);
  }

  function poblarFormulario(data) {
    const inputAnr = document.getElementById('input-anr');
    const inputFechaBase = document.getElementById('input-fecha-base');
    const inputIpc = document.getElementById("input-ipc");
    
    if (inputAnr) inputAnr.value = data.inversion.monto_anr_nominal;
    if (inputFechaBase) inputFechaBase.value = data.inversion.fecha_base;
    if (inputIpc) {
        inputIpc.value = ((data.inversion.ipc_acumulado - 1) * 100).toFixed(2);
    }
    
    const listaProductos = document.getElementById("lista-productos");
    const listaLineas = document.getElementById("lista-lineas");
    const listaIpc = document.getElementById("lista-ipc");

    if (listaProductos) { listaProductos.innerHTML = ""; data.productos.forEach(p => renderProductoRow(p)); }
    if (listaLineas) { listaLineas.innerHTML = ""; data.lineas_produccion.forEach(l => renderLineaRow(l)); }
    if (listaIpc && data.ipc_serie) {
       listaIpc.innerHTML = data.ipc_serie.map(item => `<div>Mes ${item.mes}: ${(item.tasa * 100).toFixed(1)}%</div>`).join('');
    }
  }

  function actualizarUI(results, realAnr) {
    SimulationUIUpdater.actualizarKPIs(results, realAnr);
    SimulationUIUpdater.renderizarTabla(results.resultados);
    if (ctx) renderizarGrafico(results.proyecciones, results.target_repago);
  }

  function renderizarGrafico(proyecciones, target) {
    if (window.myChart) window.myChart.destroy();
    
    const labels = Object.values(proyecciones)[0].map(p => p.fecha);
    const datasets = Object.keys(proyecciones).map((key, i) => ({
      label: key + ' (Valor Presente)',
      data: proyecciones[key].map(p => p.beneficio_acumulado_presente),
      borderColor: i === 0 ? 'rgba(75, 192, 192, 1)' : (i === 1 ? 'rgba(255, 99, 132, 1)' : 'rgba(153, 102, 255, 1)'),
      fill: false
    }));

    window.myChart = new Chart(ctx, {
      type: 'line',
      data: { labels, datasets },
      options: { 
        responsive: true, 
        maintainAspectRatio: false,
        plugins: {
            title: { display: true, text: 'Proyección de Beneficio Acumulado (Valor Presente)' }
        }
      }
    });
  }
});
