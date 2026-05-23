import { ApiClient } from './apiClient.js';

/**
 * Controlador de simulación.
 */
export const SimulationController = {
  async runSimulation(formData) {
    // Observabilidad: Validar estado antes de procesar
    if (!formData || Object.keys(formData).length === 0) {
      console.warn('[FITBA] SimulationController: Form data is empty. Proceeding, but results might be invalid.');
    }
    
    try {
      const { SimulationMapper } = await import('./simulationMapper.js');
      const payload = SimulationMapper.mapFormToPayload(formData);

      const startTime = performance.now();
      const apiResponse = await ApiClient.post('/api/v1/simulacion/ejecutar', payload);
      const endTime = performance.now();
      
      console.log(`[Observability] Simulation API call took: ${(endTime - startTime).toFixed(2)}ms`);
      return apiResponse;
    } catch (error) {
      console.error('Controller: Error in runSimulation', { error });
      throw error;
    }
  }
};
