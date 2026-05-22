/**
 * Path: src/infrastructure/web/static/js/simulationService.js
 * Lógica de Negocio: Cálculo de Proyecciones de Simulación
 */

export const SimulationService = {
  calcularProyeccionesMensuales(payload) {
    const meses = Array.from({ length: 24 }, (_, i) => i + 1);
    const dispBase = payload.oee.linea_base.disponibilidad;
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
};
