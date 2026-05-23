
import { SimulationService } from './simulationService.js';

export const SimulationDomain = {
  // Transforma los datos del DOM en el payload de la API
  mapFormToPayload(formData) {
    return {
      inversion: {
        objetivo_anr: parseFloat(formData.anr),
        factor_ipc_acumulado: (parseFloat(formData.ipc) / 100) + 1
      },
      oee: {
        linea_base: {
          disponibilidad: parseFloat(formData.dispBase) / 100,
          rendimiento: parseFloat(formData.perf) / 100,
          calidad: parseFloat(formData.quality) / 100
        },
        limite_disponibilidad: 0.85
      },
      produccion: {
        volumen_mensual_base: parseFloat(formData.volBase),
        precio_unitario_promedio: parseFloat(formData.precio),
        costos_variables: { material_por_unidad: parseFloat(formData.costo) }
      },
      escenarios: {
        desfavorable: { nombre: 'Desfavorable', tasa_crecimiento_mensual: parseFloat(formData.rateDesfavorable) / 100, factor_demanda: 1.0 },
        proyectado: { nombre: 'Proyectado', tasa_crecimiento_mensual: parseFloat(formData.rateProyectado) / 100, factor_demanda: 1.0 },
        favorable: { nombre: 'Favorable', tasa_crecimiento_mensual: parseFloat(formData.rateFavorable) / 100, factor_demanda: 1.0 }
      }
    };
  },

  // Lógica de cálculo extra para la UI (Frontend-side projection)
  calculateFrontendProjections(payload) {
    return SimulationService.calcularProyeccionesMensuales(payload);
  }
};
