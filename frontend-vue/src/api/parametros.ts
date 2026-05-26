import apiClient from './client';

export const getParametros = async () => {
  const response = await apiClient.get('/api/v1/simulacion/parametros');
  return response.data;
};
