/**
 * Responsabilidad: Actualizar la interfaz de usuario con los resultados.
 */
export const SimulationUIUpdater = {
  actualizarKPIs(results) {
    // console.log('[DEBUG] UIUpdater.actualizarKPIs, results:', results);
    
    const kpiTarget = document.getElementById('kpi-target-actualizado');
    const kpiOeeBase = document.getElementById('kpi-oee-base');
    const kpiOeeMax = document.getElementById('kpi-oee-max');
    
    if (results.target_repago !== undefined && kpiTarget) {
        kpiTarget.textContent = '$' + results.target_repago.toLocaleString('es-AR', { minimumFractionDigits: 0 });
    } else {
        // console.warn('[DEBUG] UIUpdater: target_repago missing or kpiTarget missing');
    }

    if (results.oee_base !== undefined && kpiOeeBase) {
        kpiOeeBase.textContent = (results.oee_base * 100).toFixed(2) + '%';
    }

    const inputPerf = document.getElementById('input-perf');
    const inputQuality = document.getElementById('input-quality');
    
    if (inputPerf && inputQuality && kpiOeeMax) {
        const oeeMaxVal = 0.85 * (parseFloat(inputPerf.value || 0)/100) * (parseFloat(inputQuality.value || 0)/100);
        kpiOeeMax.textContent = (oeeMaxVal * 100).toFixed(2) + '%';
    }
  },

  renderizarTabla(resultados) {
    // console.log('[DEBUG] UIUpdater.renderizarTabla, resultados:', resultados);
    const tbody = document.getElementById('resultados-tbody');
    if (!tbody) {
        // console.warn('[DEBUG] UIUpdater: tbody element not found');
        return;
    }
    
    try {
        tbody.innerHTML = '';
        resultados.forEach((res, index) => {
          // console.log(`[DEBUG] Rendering row ${index}:`, res);
          const mesText = res.mes_repago !== undefined ? 'Mes ' + res.mes_repago : 'Límite >24m';
          const viableClass = res.viable ? 'badge-favorable' : 'badge-desfavorable';
          tbody.innerHTML += '<tr>' +
            '<td><span class="badge-escenario badge-' + (res.escenario || 'default').toLowerCase() + '">' + (res.escenario || 'N/A') + '</span></td>' +
            '<td class="text-center">' + ((res.tasa || 0) * 100).toFixed(1) + '%</td>' +
            '<td class="text-center fw-bold text-white">' + mesText + '</td>' +
            '<td class="text-center"><span class="badge-escenario ' + viableClass + '">' + (res.viable ? 'Viable' : 'No Viable') + '</span></td>' +
            '</tr>';
        });
    } catch (e) {
        // console.error('[FITBA ERROR] renderizarTabla failed:', e);
    }
  }
};
