
import { SimulationService } from './simulationService.js';

export const SimulationDomain = {
  // Transforma los datos del DOM en el nuevo payload de la API
  mapFormToPayload(formData) {
    const defaultProductos = [{ id: 'p1', nombre: 'Producto A', precio_unitario: parseFloat(formData.precio), costo_marginal_unitario: parseFloat(formData.costo) }];
    const defaultLineas = [{ id: 'l1', nombre: 'Linea 1', capacidad_nominal: parseFloat(formData.volBase), productos_compatibles: ['p1'] }];
    const defaultMix = [{ producto_id: 'p1', porcentaje: 1.0 }];

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
      productos: defaultProductos,
      lineas_produccion: defaultLineas,
      mix_objetivo: defaultMix,
      escenarios: {
        desfavorable: { nombre: 'Desfavorable', tasa_crecimiento_mensual: parseFloat(formData.rateDesfavorable) / 100, factor_demanda: 1.0 },
        proyectado: { nombre: 'Proyectado', tasa_crecimiento_mensual: parseFloat(formData.rateProyectado) / 100, factor_demanda: 1.0 },
        favorable: { nombre: 'Favorable', tasa_crecimiento_mensual: parseFloat(formData.rateFavorable) / 100, factor_demanda: 1.0 }
      }
    };
  },

  // Adaptador para mantener compatibilidad con SimulationService
  calculateFrontendProjections(formData) {
    // Reconstruimos el objeto que el servicio espera
    const legacyPayload = {
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
        desfavorable: { tasa_crecimiento_mensual: parseFloat(formData.rateDesfavorable) / 100, factor_demanda: 1.0 },
        proyectado: { tasa_crecimiento_mensual: parseFloat(formData.rateProyectado) / 100, factor_demanda: 1.0 },
        favorable: { tasa_crecimiento_mensual: parseFloat(formData.rateFavorable) / 100, factor_demanda: 1.0 }
      }
    };
    return SimulationService.calcularProyeccionesMensuales(legacyPayload);
  }
};
