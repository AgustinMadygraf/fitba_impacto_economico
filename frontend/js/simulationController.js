import { ApiClient } from './apiClient.js';
import { SimulationDomain } from './simulationDomain.js?v=3';
import { SimulationMapper } from './simulationMapper.js?v=3';

/**
 * @typedef {Object} FormData
 * @property {string} anr
 * @property {string} ipc
 * @property {string} dispBase
 * @property {string} perf
 * @property {string} quality
 * @property {string} volBase
 * @property {string} precio
 * @property {string} costo
 * @property {string} rateDesfavorable
 * @property {string} rateProyectado
 * @property {string} rateFavorable
 */

/**
 * Controlador de simulación.
 */
export const SimulationController = {
  async runSimulation(formData) {
    try {
      // 1. Mapeo a DTO
      const payload = SimulationMapper.mapFormToPayload(formData);

      // 2. Ejecución Infraestructura
      const apiResponse = await ApiClient.post('/api/simular', payload);

      // 3. Ejecución Dominio
      const projections = SimulationDomain.calculateFrontendProjections(formData);
      
      return {
        ...apiResponse,
        proyecciones: projections
      };
    } catch (error) {
      if (window.APP_CONFIG && window.APP_CONFIG.mode === 'development') console.error('Controller: Error en simulación', { error });
      throw error;
    }
  }
};
