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
  const ctx = document.getElementById('chart-proyeccion').getContext('2d');
  let myChart = null;

  fetch('/api/v1/simulacion/parametros')
    .then(res => res.json())
    .then(async data => {
      poblarFormulario(data);
      loading.classList.remove('d-none');
      try {
        const formData = FormBinder.getSimulationData();
        if (getMode() === 'development') console.debug('[FITBA] Simulación inicial con datos:', formData);
        const results = await SimulationController.runSimulation(formData);
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
      const formData = FormBinder.getSimulationData();
      if (getMode() === 'development' || true) { // Forzado temporalmente para depuración solicitada
        console.group('[FITBA] Depuración de Simulación');
        console.info('1. Datos recolectados del formulario:', formData);
      }

      const results = await SimulationController.runSimulation(formData);
      
      if (getMode() === 'development' || true) {
        console.info('2. Resultados recibidos del Backend:', results);
        console.groupEnd();
      }

      actualizarUI(results);
    } catch (error) {
      console.error('[FITBA] Error crítico en simulación:', error);
      alert('Error en simulación: ' + error.message);
      if (getMode() === 'development' || true) console.groupEnd();
    } finally {
      loading.classList.add('d-none');
    }
  });

  /**
   * Renderiza dinámicamente un producto en la UI.
   * @param {Object} producto - Datos del producto.
   */
  function renderProductoRow(producto = { id: Date.now().toString(), nombre: "Nuevo Producto", precio: 0, costo: 0 }) {
    const container = document.getElementById("lista-productos");
    const div = document.createElement("div");
    div.className = "card mb-2 p-2 border-0 bg-dark bg-opacity-10 item-producto";
    div.dataset.id = producto.id;
    div.innerHTML = `
      <input type="text" class="form-control mb-1 input-producto-nombre" value="${producto.nombre}" placeholder="Nombre">
      <div class="d-flex gap-2">
        <input type="number" step="0.1" class="form-control input-producto-precio" value="${producto.precio}" placeholder="Precio">
        <input type="number" step="0.1" class="form-control input-producto-costo" value="${producto.costo}" placeholder="Costo">
      </div>
    `;
    container.appendChild(div);
    
    // Alcance Inicial: Restringir a 1 producto
    if (container.children.length >= 1) {
      document.getElementById("add-producto").disabled = true;
    }
  }

  /**
   * Renderiza dinámicamente una línea de producción en la UI.
   * @param {Object} linea - Datos de la línea.
   */
  function renderLineaRow(linea = { id: Date.now().toString(), nombre: "Línea 1", capacidad: 0 }) {
    const container = document.getElementById("lista-lineas");
    const div = document.createElement("div");
    div.className = "card mb-2 p-2 border-0 bg-dark bg-opacity-10 item-linea";
    div.dataset.id = linea.id;
    div.innerHTML = `
      <input type="text" class="form-control mb-1 input-linea-nombre" value="${linea.nombre}" placeholder="Nombre">
      <input type="number" step="1000" class="form-control input-linea-capacidad" value="${linea.capacidad}" placeholder="Capacidad Nominal">
    `;
    container.appendChild(div);

    // Alcance Inicial: Restringir a 1 línea
    if (container.children.length >= 1) {
      document.getElementById("add-linea").disabled = true;
    }
  }

  /**
  * Pobla el formulario con datos iniciales.
  * @param {Object} data - Datos iniciales.
  */
  function poblarFormulario(data) {
    if (!data.inversion || !data.productos || !data.lineas_produccion) {
        console.error("Error: Contrato API violado, faltan campos en la respuesta", data);
        return;
    }

    document.getElementById('input-anr').value = data.inversion.monto_actualizado;
    document.getElementById('input-ipc').value = 0; 
    
    document.getElementById("input-quality").value = (data.oee.calidad * 100).toFixed(1);
    document.getElementById('input-disp-base').value = (data.oee.disponibilidad * 100).toFixed(1);
    document.getElementById('input-perf').value = (data.oee.rendimiento * 100).toFixed(1);
    
    // Limpiar contenedores
    document.getElementById("lista-productos").innerHTML = "";
    document.getElementById("lista-lineas").innerHTML = "";

    // Poblar productos
    data.productos.forEach(p => {
      renderProductoRow({
        id: p.id,
        nombre: p.nombre,
        precio: p.precio_unitario,
        costo: p.costo_marginal_unitario
      });
    });

    // Poblar líneas
    data.lineas_produccion.forEach(l => {
      renderLineaRow({
        id: l.id,
        nombre: l.nombre,
        capacidad: l.capacidad_nominal
      });
    });
    
    // Mantener campos legacy por compatibilidad temporal con FormBinder
    document.getElementById('input-precio').value = data.productos[0].precio_unitario;
    document.getElementById('input-costo').value = data.productos[0].costo_marginal_unitario;
    document.getElementById('input-vol-base').value = data.lineas_produccion[0].capacidad_nominal;
    
    document.getElementById('input-rate-desfavorable').value = 1.0;
    document.getElementById('input-rate-proyectado').value = 1.5;
    document.getElementById('input-rate-favorable').value = 2.0;
  }

  /**
   * Actualiza la UI con los resultados.
   * @param {Object} results - Resultados de la simulación.
   */
  function actualizarUI(results) {
    UIUpdater.actualizarKPIs(results);
    UIUpdater.renderizarTabla(results.resultados);
    renderizarGrafico(results.proyecciones, results.target_repago);
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
