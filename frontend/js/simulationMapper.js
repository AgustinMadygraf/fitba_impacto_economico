/**
 * DTO Mapper: Transforma datos del UI Form a API Payload (DTO).
 */
export const SimulationMapper = {
  mapFormToPayload(formData) {
    const parseFloatOrDefault = (val, def = 0) => {
      const parsed = parseFloat(val);
      return isNaN(parsed) ? def : parsed;
    };

    const inversion = {
      objetivo_anr: parseFloatOrDefault(formData.anr, 0),
      factor_ipc_acumulado: 1.0 
    };

    const oee = {
      disponibilidad: parseFloatOrDefault(formData.dispBase, 0) / 100,
      rendimiento: parseFloatOrDefault(formData.perf, 0) / 100,
      calidad: parseFloatOrDefault(formData.quality, 0) / 100
    };

    const productos = formData.productos.map(p => ({
      id: p.id,
      nombre: p.nombre,
      precio_unitario: parseFloatOrDefault(p.precio, 0),
      costo_marginal_unitario: parseFloatOrDefault(p.costo, 0)
    }));

    const lineas_produccion = formData.lineas.map(l => ({
      id: l.id,
      nombre: l.nombre,
      capacidad_nominal: parseFloatOrDefault(l.capacidad, 0),
      productos_compatibles: productos.map(p => p.id)
    }));

    const mix_objetivo = productos.map(p => ({
      producto_id: p.id,
      porcentaje: productos.length > 0 ? (1.0 / productos.length) : 1.0
    }));

    const escenarios = {
      desfavorable: { nombre: 'Desfavorable', tasa_crecimiento_mensual: parseFloatOrDefault(formData.rateDesfavorable, 0) / 100, factor_demanda: 1.0 },
      proyectado: { nombre: 'Proyectado', tasa_crecimiento_mensual: parseFloatOrDefault(formData.rateProyectado, 0) / 100, factor_demanda: 1.0 },
      favorable: { nombre: 'Favorable', tasa_crecimiento_mensual: parseFloatOrDefault(formData.rateFavorable, 0) / 100, factor_demanda: 1.0 }
    };

    return { inversion, oee, productos, lineas_produccion, mix_objetivo, escenarios };
  }
};
