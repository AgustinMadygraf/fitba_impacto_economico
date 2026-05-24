import { ApiClient } from './apiClient.js';

export const SimulationController = {
  async runSimulation(formData) {
    console.log('[FITBA] Controller: Iniciando simulación', { formData });
    try {
      if (!formData) {
        console.error('[FITBA] Controller: Error, no hay datos del formulario');
        throw new Error('No form data provided');
      }
      
      const { SimulationMapper } = await import('./simulationMapper.js');
      const payload = SimulationMapper.mapFormToPayload(formData);

      console.debug('[FITBA] Controller: Payload preparado', payload);

      const startTime = performance.now();
      const apiResponse = await ApiClient.post('/api/v1/simulacion/ejecutar', payload);
      const endTime = performance.now();
      
      console.log('[FITBA] Controller: Simulación finalizada exitosamente', {
        duration: `${(endTime - startTime).toFixed(2)}ms`
      });
      return apiResponse;
    } catch (error) {
      console.error('[FITBA] Controller: Error en runSimulation', error);
      throw error; // Propagate for UI handling
    }
  }
};
