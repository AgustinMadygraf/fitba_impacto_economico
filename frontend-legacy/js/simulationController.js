import { ApiClient } from './apiClient.js';

export const SimulationController = {
  async runSimulation(formData) {
    try {
      if (!formData) {
        console.error('[FITBA] Controller: Error, no hay datos del formulario');
        throw new Error('No form data provided');
      }
      
      const { SimulationMapper } = await import('./simulationMapper.js');
      const payload = SimulationMapper.mapFormToPayload(formData);

      const startTime = performance.now();
      const apiResponse = await ApiClient.post('/api/v1/simulacion/ejecutar', payload);
      const endTime = performance.now();
      
      return apiResponse;
    } catch (error) {
      console.error('[FITBA] Controller: Error en runSimulation', error);
      throw error; // Propagate for UI handling
    }
  }
};
