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
      fecha_base: formData.fechaBase
    };

    const oee_base = {
      disponibilidad: parseFloatOrDefault(formData.dispBase, 0) / 100,
      rendimiento: parseFloatOrDefault(formData.perf, 0) / 100,
      calidad: parseFloatOrDefault(formData.quality, 0) / 100,
      limite_disponibilidad: 0.85
    };

    const productos = formData.productos.map(p => ({
      id: p.id,
      nombre: p.nombre,
      precio_unitario: parseFloatOrDefault(p.precio, 0),
      costo_marginal_unitario: parseFloatOrDefault(p.costo, 0)
    }));

    const lineas = formData.lineas.map(l => ({
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

    const capacidad_instalada = {
      capacidad_nominal_por_hora: 2500.0,
      horas_por_turno: 8,
      turnos_por_dia: 1,
      dias_habiles_por_mes: 22,
      dias_inhabiles_mensuales: 1
    };

    const payload = { 
        inversion, 
        oee_base, 
        catalogo: { productos, lineas }, 
        mix_objetivo, 
        escenarios,
        capacidad_instalada,
        ipc: parseFloatOrDefault(formData.ipc, 0) / 100
    };
    
    return payload;
  }
};
