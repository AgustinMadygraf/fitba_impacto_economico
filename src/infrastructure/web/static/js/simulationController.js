import { ApiClient } from './apiClient.js';
import { SimulationDomain } from './simulationDomain.js';
import { Logger } from './logger.js';

export const SimulationController = {
  async runSimulation(formData) {
    Logger.info('Iniciando coordinación de simulación...');
    try {
      const payload = SimulationDomain.mapFormToPayload(formData);
      const apiResponse = await ApiClient.post('/api/simular', payload);
      const projections = SimulationDomain.calculateFrontendProjections(payload);
      
      Logger.info('Simulación coordinada exitosamente.');
      return {
        targetRepago: apiResponse.target_repago,
        oeeBase: apiResponse.oee_base,
        resultados: apiResponse.resultados,
        proyecciones: projections
      };
    } catch (error) {
      Logger.error('Error en la coordinación de simulación', { error });
      throw error;
    }
  }
};
