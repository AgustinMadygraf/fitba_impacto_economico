/**
 * DTO Mapper: Transforma datos del UI Form a API Payload (DTO).
 * Responsabilidad única (SOLID - SRP).
 */
export const SimulationMapper = {
  /**
   * Mapea los datos del formulario a un payload DTO.
   * @param {Object} formData - Los datos recolectados del formulario.
   * @returns {Object} El payload para la API.
   */
  mapFormToPayload(formData) {
    const inversion = {
      objetivo_anr: parseFloat(formData.anr),
      factor_ipc_acumulado: 1.0 // MVP: Valor Presente, no aplica IPC adicional
    };

    const oee = {
      disponibilidad: parseFloat(formData.dispBase) / 100,
      rendimiento: parseFloat(formData.perf) / 100,
      calidad: parseFloat(formData.quality) / 100
    };

    const productos = formData.productos.map(p => ({
      id: p.id,
      nombre: p.nombre,
      precio_unitario: p.precio,
      costo_marginal_unitario: p.costo
    }));

    const lineas_produccion = formData.lineas.map(l => ({
      id: l.id,
      nombre: l.nombre,
      capacidad_nominal: l.capacidad,
      productos_compatibles: productos.map(p => p.id) // Todos compatibles por ahora
    }));

    const mix_objetivo = productos.map(p => ({
      producto_id: p.id,
      porcentaje: 1.0 / productos.length // Mix equitativo por defecto
    }));

    const escenarios = {
      desfavorable: { nombre: 'Desfavorable', tasa_crecimiento_mensual: parseFloat(formData.rateDesfavorable) / 100, factor_demanda: 1.0 },
      proyectado: { nombre: 'Proyectado', tasa_crecimiento_mensual: parseFloat(formData.rateProyectado) / 100, factor_demanda: 1.0 },
      favorable: { nombre: 'Favorable', tasa_crecimiento_mensual: parseFloat(formData.rateFavorable) / 100, factor_demanda: 1.0 }
    };

    return { inversion, oee, productos, lineas_produccion, mix_objetivo, escenarios };
  }
};
