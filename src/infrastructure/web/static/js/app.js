/**
 * Path: src/infrastructure/web/static/js/app.js
 */

import { SimulationService } from './simulationService.js';

document.addEventListener('DOMContentLoaded', () => {
  // 1. Instanciación de Controles DOM
  const form = document.getElementById('form-simulacion');
  const inputAnr = document.getElementById('input-anr');
  const inputIpc = document.getElementById('input-ipc');
  const inputDispBase = document.getElementById('input-disp-base');
  const inputPerf = document.getElementById('input-perf');
  const inputQuality = document.getElementById('input-quality');
  const inputVolBase = document.getElementById('input-vol-base');
  const inputPrecio = document.getElementById('input-precio');
  const inputCosto = document.getElementById('input-costo');

  const inputRateDesfavorable = document.getElementById('input-rate-desfavorable');
  const inputRateProyectado = document.getElementById('input-rate-proyectado');
  const inputRateFavorable = document.getElementById('input-rate-favorable');

  // KPIs (Sección 2: Datos Intermedios)
  const kpiTargetActualizado = document.getElementById('kpi-target-actualizado');
  const kpiOeeBase = document.getElementById('kpi-oee-base');
  const kpiOeeMax = document.getElementById('kpi-oee-max');

  // Containers (Sección 3: Salidas)
  const loading = document.getElementById('loading');
  const resultadosTbody = document.getElementById('resultados-tbody');

  // 2. Inicialización del Gráfico Chart.js
  const ctx = document.getElementById('chart-proyeccion').getContext('2d');
  let myChart = null;

  // Cargar Parámetros Base al Iniciar
  fetch('/api/params')
    .then(res => {
      if (!res.ok) throw new Error('Error al consultar API');
      return res.json();
    })
    .then(data => {
      poblarFormulario(data);
      ejecutarSimulacion(prepararPayload());
    })
    .catch(err => {
      console.error('Error inicializando parámetros:', err);
    });

  // Manejar Envío del Formulario
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    ejecutarSimulacion(prepararPayload());
  });

  // Funciones de Apoyo
  function poblarFormulario(data) {
    inputAnr.value = data.inversion.objetivo_anr;
    inputIpc.value = ((data.inversion.factor_ipc_acumulado - 1) * 100).toFixed(1);
    inputDispBase.value = (data.oee.linea_base.disponibilidad * 100).toFixed(1);
    inputPerf.value = (data.oee.linea_base.rendimiento * 100).toFixed(1);
    inputQuality.value = (data.oee.linea_base.calidad * 100).toFixed(1);
    inputVolBase.value = data.produccion.volumen_mensual_base;
    inputPrecio.value = data.produccion.precio_unitario_promedio;
    inputCosto.value = data.produccion.costos_variables.material_por_unidad;
    inputRateDesfavorable.value = (data.escenarios.desfavorable.tasa_crecimiento_mensual * 100).toFixed(1);
    inputRateProyectado.value = (data.escenarios.proyectado.tasa_crecimiento_mensual * 100).toFixed(1);
    inputRateFavorable.value = (data.escenarios.favorable.tasa_crecimiento_mensual * 100).toFixed(1);
  }

  function prepararPayload() {
    return {
      inversion: {
        objetivo_anr: parseFloat(inputAnr.value),
        factor_ipc_acumulado: (parseFloat(inputIpc.value) / 100) + 1
      },
      oee: {
        linea_base: {
          disponibilidad: parseFloat(inputDispBase.value) / 100,
          rendimiento: parseFloat(inputPerf.value) / 100,
          calidad: parseFloat(inputQuality.value) / 100
        },
        limite_disponibilidad: 0.85
      },
      produccion: {
        volumen_mensual_base: parseFloat(inputVolBase.value),
        precio_unitario_promedio: parseFloat(inputPrecio.value),
        costos_variables: { material_por_unidad: parseFloat(inputCosto.value) }
      },
      escenarios: {
        desfavorable: { nombre: 'Desfavorable', tasa_crecimiento_mensual: parseFloat(inputRateDesfavorable.value) / 100, factor_demanda: 1.0 },
        proyectado: { nombre: 'Proyectado', tasa_crecimiento_mensual: parseFloat(inputRateProyectado.value) / 100, factor_demanda: 1.0 },
        favorable: { nombre: 'Favorable', tasa_crecimiento_mensual: parseFloat(inputRateFavorable.value) / 100, factor_demanda: 1.0 }
      }
    };
  }

  function ejecutarSimulacion(payload) {
    loading.classList.remove('d-none');
    fetch('/api/simular', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(res => res.json())
      .then(apiResponse => {
        actualizarDatosIntermedios(apiResponse);
        actualizarSalidas(apiResponse, payload);
        loading.classList.add('d-none');
      })
      .catch(err => {
        console.error(err);
        loading.classList.add('d-none');
      });
  }

  function actualizarDatosIntermedios(res) {
    kpiTargetActualizado.textContent = '$' + res.target_repago.toLocaleString('es-AR', { minimumFractionDigits: 0 });
    kpiOeeBase.textContent = (res.oee_base * 100).toFixed(2) + '%';
    const oeeMaxVal = 0.85 * (parseFloat(inputPerf.value)/100) * (parseFloat(inputQuality.value)/100);
    kpiOeeMax.textContent = (oeeMaxVal * 100).toFixed(2) + '%';
  }

  function actualizarSalidas(res, payload) {
    renderizarTabla(res.resultados);
    const proyeccionesGrafico = SimulationService.calcularProyeccionesMensuales(payload);
    renderizarGrafico(proyeccionesGrafico, res.target_repago);
  }

  function renderizarTabla(resultados) {
    resultadosTbody.innerHTML = '';
    resultados.forEach(res => {
      const mesText = res.mes_repago ? 'Mes ' + res.mes_repago : 'Límite >24m';
      const viableClass = res.viable ? 'badge-favorable' : 'badge-desfavorable';
      const row = '<tr>' +
        '<td><span class="badge-escenario badge-' + res.escenario.toLowerCase() + '">' + res.escenario + '</span></td>' +
        '<td class="text-center">' + (res.tasa * 100).toFixed(1) + '%</td>' +
        '<td class="text-center fw-bold text-white">' + mesText + '</td>' +
        '<td class="text-center"><span class="badge-escenario ' + viableClass + '">' + (res.viable ? 'Viable' : 'No Viable') + '</span></td>' +
        '</tr>';
      resultadosTbody.innerHTML += row;
    });
  }

  function renderizarGrafico(proyecciones, target) {
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
            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#888', callback: v => '$' + (v / 1e6).toFixed(1) + 'M' } }
          }
        }
      });
    }
  }
});
