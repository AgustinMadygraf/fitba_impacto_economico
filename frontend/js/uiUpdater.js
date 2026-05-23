/**
 * Responsabilidad: Actualizar la interfaz de usuario con los resultados.
 */
export const UIUpdater = {
  actualizarKPIs(results) {
    document.getElementById('kpi-target-actualizado').textContent = '$' + results.target_repago.toLocaleString('es-AR', { minimumFractionDigits: 0 });
    document.getElementById('kpi-oee-base').textContent = (results.oee_base * 100).toFixed(2) + '%';
    
    const oeeMaxVal = 0.85 * (parseFloat(document.getElementById('input-perf').value)/100) * (parseFloat(document.getElementById('input-quality').value)/100);
    document.getElementById('kpi-oee-max').textContent = (oeeMaxVal * 100).toFixed(2) + '%';
  },

  renderizarTabla(resultados) {
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
};
