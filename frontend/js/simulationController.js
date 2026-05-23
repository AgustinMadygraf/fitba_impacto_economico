import { ApiClient } from './apiClient.js';

export const SimulationController = {
  async runSimulation(formData) {
    try {
      if (!formData) throw new Error("No form data provided");
      
      const { SimulationMapper } = await import('./simulationMapper.js');
      const payload = SimulationMapper.mapFormToPayload(formData);

      // console.debug('[DEBUG] Controller: Final payload before API:', payload);

      const startTime = performance.now();
      const apiResponse = await ApiClient.post('/api/v1/simulacion/ejecutar', payload);
      const endTime = performance.now();
      
      // console.debug(`[Observability] Simulation API call took: ${(endTime - startTime).toFixed(2)}ms`);
      return apiResponse;
    } catch (error) {
      // console.error('[FITBA] Controller: Error in runSimulation', error);
      throw error; // Propagate for UI handling
    }
  }
};
