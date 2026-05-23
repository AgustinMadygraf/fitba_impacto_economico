/**
 * DTO Mapper: Transforma datos del UI Form a API Payload (DTO).
 * Responsabilidad única (SOLID - SRP).
 */
export const SimulationMapper = {
/**
 * Mapea los datos del formulario a un payload DTO.
 * @param {FormData} formData - Los datos recolectados del formulario.
 * @returns {Object} El payload para la API.
 */
  mapFormToPayload(formData) {
    const inversion = {
      objetivo_anr: parseFloat(formData.anr),
      factor_ipc_acumulado: 1.0 // MVP: Valor Presente, no aplica IPC adicional
    };

    // CORRECCIÓN: Estructura plana que espera el backend ahora
    const oee = {
      disponibilidad: parseFloat(formData.dispBase) / 100,
      rendimiento: parseFloat(formData.perf) / 100,
      calidad: parseFloat(formData.quality) / 100
    };

    const productos = [{ 
      id: 'p1', 
      nombre: 'Producto A', 
      precio_unitario: parseFloat(formData.precio), 
      costo_marginal_unitario: parseFloat(formData.costo) 
    }];
    
    // MVP: Mantener estructura obligatoria para Pydantic
    const lineas_produccion = [{ 
      id: 'l1', 
      nombre: 'Linea 1', 
      capacidad_nominal: parseFloat(formData.volBase) || 0, 
      productos_compatibles: ['p1'] 
    }];

    const mix_objetivo = [{ producto_id: 'p1', porcentaje: 1.0 }];

    const escenarios = {
      desfavorable: { nombre: 'Desfavorable', tasa_crecimiento_mensual: parseFloat(formData.rateDesfavorable) / 100, factor_demanda: 1.0 },
      proyectado: { nombre: 'Proyectado', tasa_crecimiento_mensual: parseFloat(formData.rateProyectado) / 100, factor_demanda: 1.0 },
      favorable: { nombre: 'Favorable', tasa_crecimiento_mensual: parseFloat(formData.rateFavorable) / 100, factor_demanda: 1.0 }
    };

    return { inversion, oee, productos, lineas_produccion, mix_objetivo, escenarios };
  }
};
