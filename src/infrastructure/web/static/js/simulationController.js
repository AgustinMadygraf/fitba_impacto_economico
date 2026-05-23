import { ApiClient } from './apiClient.js';
import { SimulationDomain } from './simulationDomain.js';
import { Logger } from './logger.js';

export const SimulationController = {
  async runSimulation(formData) {
    const timerLabel = 'Simulación Total';
    Logger.time(timerLabel);
    Logger.info('Controller: Mapeando formulario...');
    
    try {
      const payload = SimulationDomain.mapFormToPayload(formData);
      
      const apiResponse = await ApiClient.post('/api/simular', payload);
      
      const projections = SimulationDomain.calculateFrontendProjections(formData);
      
      Logger.timeEnd(timerLabel);
      
      return {
        targetRepago: apiResponse.target_repago,
        oeeBase: apiResponse.oee_base,
        resultados: apiResponse.resultados,
        proyecciones: projections
      };
    } catch (error) {
      Logger.timeEnd(timerLabel);
      Logger.error('Controller: Error crítico', { error });
      throw error;
    }
  }
};