/**
 * Path: src/infrastructure/web/static/js/simulationDashboard.js
 */

import { SimulationController } from './simulationController.js';
import { FormBinder } from './formBinder.js';
import { UIUpdater } from './uiUpdater.js';
import { UINotifier } from './uiNotifier.js';

document.addEventListener('DOMContentLoaded', async () => {
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
        console.error("[FITBA ERROR] Simulation failed:", error);
      } finally {
        if (loading) loading.classList.add('d-none');
      }
    });

  form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (loading) loading.classList.remove('d-none');
    try {
      const formData = FormBinder.getSimulationData();
      const results = await SimulationController.runSimulation(formData);
      actualizarUI(results);
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
    div.dataset.id = producto.id;
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
    div.dataset.id = linea.id;
    div.innerHTML = `
      <input type="text" class="form-control mb-1 input-linea-nombre" value="${linea.nombre}" placeholder="Nombre">
      <input type="number" step="1000" class="form-control input-linea-capacidad" value="${linea.capacidad_nominal || 0}" placeholder="Capacidad Nominal">
    `;
    container.appendChild(div);
  }

  function poblarFormulario(data) {
    const inputAnr = document.getElementById('input-anr');
    const inputFechaBase = document.getElementById('input-fecha-base');
    if (inputAnr) inputAnr.value = data.inversion.monto_actualizado;
    if (inputFechaBase) inputFechaBase.value = data.inversion.fecha_base;
    
    const listaProductos = document.getElementById("lista-productos");
    const listaLineas = document.getElementById("lista-lineas");
    const listaIpc = document.getElementById("lista-ipc");

    if (listaProductos) { listaProductos.innerHTML = ""; data.productos.forEach(p => renderProductoRow(p)); }
    if (listaLineas) { listaLineas.innerHTML = ""; data.lineas_produccion.forEach(l => renderLineaRow(l)); }
    if (listaIpc && data.ipc_serie) {
       listaIpc.innerHTML = data.ipc_serie.map(item => `<div>Mes ${item.mes}: ${(item.tasa * 100).toFixed(1)}%</div>`).join('');
    }
  }

  function actualizarUI(results) {
    UIUpdater.actualizarKPIs(results);
    UIUpdater.renderizarTabla(results.resultados);
    if (ctx) renderizarGrafico(results.proyecciones, results.target_repago);
  }

  function renderizarGrafico(proyecciones, target) {
    if (myChart) myChart.destroy();
    
    const labels = Object.values(proyecciones)[0].map(p => p.fecha);
    const datasets = Object.keys(proyecciones).map((key, i) => ({
      label: key,
      data: proyecciones[key].map(p => p.beneficio_acumulado),
      borderColor: i === 0 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)',
      fill: false
    }));

    myChart = new Chart(ctx, {
      type: 'line',
      data: { labels, datasets },
      options: { responsive: true, maintainAspectRatio: false }
    });
  }
});
