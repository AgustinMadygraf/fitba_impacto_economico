import { ApiClient } from './apiClient.js';

/**
 * Controlador de simulación.
 */
export const SimulationController = {
  async runSimulation(formData) {
    try {
      // 1. Mapeo a DTO (se mantiene por ahora en SimulationMapper)
      const { SimulationMapper } = await import('./simulationMapper.js');
      const payload = SimulationMapper.mapFormToPayload(formData);

      // 2. Ejecución Infraestructura (Backend centralizado)
      const apiResponse = await ApiClient.post('/api/v1/simulacion/ejecutar', payload);
      
      // 3. Ya no necesitamos SimulationDomain ni SimulationService en el frontend
      // para el cálculo de proyecciones, el backend las provee.
      
      return apiResponse;
    } catch (error) {
      if (window.APP_CONFIG && window.APP_CONFIG.mode === 'development') console.error('Controller: Error en simulación', { error });
      throw error;
    }
  }
};
