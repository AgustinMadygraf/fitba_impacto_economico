/**
 * Dominio: Lógica de Negocio Pura (Proyecciones).
 * Independiente de UI y API (Clean Architecture).
 */
import { SimulationService } from './simulationService.js';

export const SimulationDomain = {
  // Solo lógica de dominio, sin mapeo de DTOs
  calculateFrontendProjections(formData) {
    // El servicio necesita la estructura legacy, aquí sí es válido el mapper interno
    // porque es un adaptador de dominio a servicio.
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
