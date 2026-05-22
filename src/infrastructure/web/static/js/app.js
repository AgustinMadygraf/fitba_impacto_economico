/**
 * Path: src/infrastructure/web/static/js/app.js
 * Lógica del Frontend y Visualización Dinámica FITBA
 */

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
  
  // KPIs
  const kpiTargetActualizado = document.getElementById('kpi-target-actualizado');
  const kpiOeeBase = document.getElementById('kpi-oee-base');
  const kpiOeeMax = document.getElementById('kpi-oee-max');
  
  // Containers
  const loading = document.getElementById('loading');
  const tableContainer = document.getElementById('table-container');
  const resultadosTbody = document.getElementById('resultados-tbody');
  
  // 2. Inicialización del Gráfico Chart.js
  const ctx = document.getElementById('chart-proyeccion').getContext('2d');
  let myChart = null;

  // Cargar Parámetros Base al Iniciar
  fetch('/api/params')
    .then(res => {
      if (!res.ok) throw new Error("Error al consultar API");
      return res.json();
    })
    .then(data => {
      // Poblar Inputs
      inputAnr.value = data.inversion.objetivo_anr;
      inputIpc.value = data.inversion.factor_ipc_acumulado;
      inputDispBase.value = data.oee.linea_base.disponibilidad;
      inputPerf.value = data.oee.linea_base.rendimiento;
      inputQuality.value = data.oee.linea_base.calidad;
      
      inputVolBase.value = data.produccion.volumen_mensual_base;
      inputPrecio.value = data.produccion.precio_unitario_promedio;
      inputCosto.value = data.produccion.costos_variables.material_por_unidad;
      
      inputRateDesfavorable.value = data.escenarios.desfavorable.tasa_crecimiento_mensual;
      inputRateProyectado.value = data.escenarios.proyectado.tasa_crecimiento_mensual;
      inputRateFavorable.value = data.escenarios.favorable.tasa_crecimiento_mensual;
      
      kpiOeeMax.textContent = `${(data.oee.limite_disponibilidad * data.oee.linea_base.rendimiento * data.oee.linea_base.calidad * 100).toFixed(2)}%`;

      // Primera simulación inicial
      ejecutarSimulacion(data);
    })
    .catch(err => {
      console.error("Error inicializando parámetros:", err);
      alert("No se pudo conectar con la API de simulación. Asegúrate de que el servidor FastAPI esté corriendo.");
    });

  // Manejar Envío del Formulario
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    // Armar Payload a partir del DOM
    const payload = {
      inversion: {
        objetivo_anr: parseFloat(inputAnr.value),
        factor_ipc_acumulado: parseFloat(inputIpc.value)
      },
      oee: {
        linea_base: {
          disponibilidad: parseFloat(inputDispBase.value),
          rendimiento: parseFloat(inputPerf.value),
          calidad: parseFloat(inputQuality.value)
        },
        limite_disponibilidad: 0.85 // Límite físico por defecto
      },
      produccion: {
        volumen_mensual_base: parseFloat(inputVolBase.value),
        precio_unitario_promedio: parseFloat(inputPrecio.value),
        costos_variables: {
          material_por_unidad: parseFloat(inputCosto.value)
        }
      },
      escenarios: {
        desfavorable: {
          nombre: "Desfavorable",
          tasa_crecimiento_mensual: parseFloat(inputRateDesfavorable.value),
          factor_demanda: 1.0
        },
        proyectado: {
          nombre: "Proyectado",
          tasa_crecimiento_mensual: parseFloat(inputRateProyectado.value),
          factor_demanda: 1.0
        },
        favorable: {
          nombre: "Favorable",
          tasa_crecimiento_mensual: parseFloat(inputRateFavorable.value),
          factor_demanda: 1.0
        }
      }
    };

    ejecutarSimulacion(payload);
  });

  // Función Central de Simulación
  function ejecutarSimulacion(payload) {
    loading.classList.remove('d-none');
    tableContainer.classList.add('d-opacity-50');

    // 1. Llamada a la API backend para cálculo de repago oficial
    fetch('/api/simular', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(res => {
        if (!res.ok) throw new Error("Error en la simulación");
        return res.json();
      })
      .then(apiResponse => {
        // Actualizar KPIs Rápidos
        const target = apiResponse.target_repago;
        kpiTargetActualizado.textContent = `$${target.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        
        const oeeBaseVal = apiResponse.oee_base;
        kpiOeeBase.textContent = `${(oeeBaseVal * 100).toFixed(2)}%`;

        // Renderizar tabla
        renderizarTabla(apiResponse.resultados);

        // 2. Calcular integral de beneficios mensual en frontend para gráfico detallado
        const proyeccionesGrafico = calcularProyeccionesMensuales(payload);
        renderizarGrafico(proyeccionesGrafico, target);

        loading.classList.add('d-none');
        tableContainer.classList.remove('d-opacity-50');
      })
      .catch(err => {
        console.error(err);
        loading.classList.add('d-none');
        alert("Ocurrió un error al ejecutar la simulación.");
      });
  }

  // Renderizar la grilla de resultados
  function renderizarTabla(resultados) {
    resultadosTbody.innerHTML = '';
    
    resultados.forEach(res => {
      const mesText = res.mes_repago ? `Mes ${res.mes_repago}` : 'Fuera de horizonte (>24 meses)';
      const viableClass = res.viable ? 'badge-favorable' : 'badge-desfavorable';
      const viableText = res.viable ? 'Viable' : 'No Viable';
      const tasaPercent = (res.tasa * 100).toFixed(2);
      
      const row = `
        <tr class="fade-in">
          <td><span class="badge-escenario badge-${res.escenario.toLowerCase()}">${res.escenario}</span></td>
          <td class="text-center fw-semibold text-white-50">${tasaPercent}%</td>
          <td class="text-center fw-bold text-white">${mesText}</td>
          <td class="text-center"><span class="badge-escenario ${viableClass}">${viableText}</span></td>
        </tr>
      `;
      resultadosTbody.innerHTML += row;
    });
  }

  // Calcular la proyección acumulada de 24 meses
  function calcularProyeccionesMensuales(payload) {
    const meses = Array.from({ length: 24 }, (_, i) => i + 1);
    const dispBase = payload.oee.linea_base.disponibilidad;
    const rendimiento = payload.oee.linea_base.rendimiento;
    const calidad = payload.oee.linea_base.calidad;
    const volBase = payload.produccion.volumen_mensual_base;
    const margen = payload.produccion.precio_unitario_promedio - payload.produccion.costos_variables.material_por_unidad;
    const limiteDisp = payload.oee.limite_disponibilidad || 0.85;

    const proyecciones = { desfavorable: [], proyectado: [], favorable: [] };

    ['desfavorable', 'proyectado', 'favorable'].forEach(key => {
      const esc = payload.escenarios[key];
      let disp_t = dispBase;
      let acumulado = 0;

      for (let m = 1; m <= 24; m++) {
        disp_t *= (1 + esc.tasa_crecimiento_mensual);
        
        // Limitar por capacidad física instalada
        const disp_activa = Math.min(disp_t, limiteDisp);
        
        // Push Model: Pt = volumen_base * (Dt / D0)
        const vol_t = volBase * (disp_activa / dispBase) * esc.factor_demanda;
        
        // Beneficio mensual marginal
        const delta_vol = vol_t - volBase;
        const ben_mensual = delta_vol * margen;

        if (ben_mensual > 0) {
          acumulado += ben_mensual;
        }
        proyecciones[key].push(acumulado);
      }
    });

    return proyecciones;
  }

  // Dibujar/Actualizar Gráfico Chart.js
  function renderizarGrafico(proyecciones, target) {
    const labels = Array.from({ length: 24 }, (_, i) => `Mes ${i + 1}`);

    // Línea segmentada constante del target
    const targetData = Array(24).fill(target);

    const datasets = [
      {
        label: 'Escenario Favorable',
        data: proyecciones.favorable,
        borderColor: 'hsl(145, 80%, 45%)',
        backgroundColor: 'hsla(145, 80%, 45%, 0.1)',
        borderWidth: 3,
        tension: 0.3,
        fill: false
      },
      {
        label: 'Escenario Proyectado',
        data: proyecciones.proyectado,
        borderColor: 'hsl(195, 100%, 50%)',
        backgroundColor: 'hsla(195, 100%, 50%, 0.1)',
        borderWidth: 3,
        tension: 0.3,
        fill: false
      },
      {
        label: 'Escenario Desfavorable',
        data: proyecciones.desfavorable,
        borderColor: 'hsl(25, 95%, 50%)',
        backgroundColor: 'hsla(25, 95%, 50%, 0.1)',
        borderWidth: 2,
        tension: 0.3,
        fill: false
      },
      {
        label: 'Target de Repago',
        data: targetData,
        borderColor: 'rgba(255, 99, 132, 0.75)',
        borderWidth: 2,
        borderDash: [6, 6],
        pointRadius: 0,
        fill: false
      }
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
          plugins: {
            legend: {
              labels: {
                color: 'hsl(215, 15%, 72%)',
                font: { family: 'Plus Jakarta Sans', size: 11 }
              }
            },
            tooltip: {
              mode: 'index',
              intersect: false,
              callbacks: {
                label: function(context) {
                  let label = context.dataset.label || '';
                  if (label) label += ': ';
                  if (context.raw !== null) {
                    label += '$' + context.raw.toLocaleString('es-AR', { maximumFractionDigits: 0 });
                  }
                  return label;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: { color: 'hsl(215, 12%, 50%)', font: { family: 'Plus Jakarta Sans' } }
            },
            y: {
              grid: { color: 'rgba(255, 255, 255, 0.05)' },
              ticks: {
                color: 'hsl(215, 12%, 50%)',
                font: { family: 'Plus Jakarta Sans' },
                callback: function(value) {
                  return '$' + (value / 1e6).toFixed(1) + 'M';
                }
              }
            }
          }
        }
      });
    }
  }
});
