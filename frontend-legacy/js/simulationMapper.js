/**
 * DTO Mapper: Transforma datos del UI Form a API Payload (DTO).
 */
export const SimulationMapper = {
  mapFormToPayload(formData) {
    const parseFloatOrDefault = (val, def = 0) => {
      const parsed = parseFloat(val);
      return isNaN(parsed) ? def : parsed;
    };

    // Mapeo explicito: formData.productos tiene objetos con {id: sku_valor, ...}
    // El Mapper debe tomar ese 'id' y convertirlo en 'sku' para la API
    const productos = formData.productos.map(p => {
        return {
            sku: p.id, 
            nombre: p.nombre,
            precio_unitario: parseFloatOrDefault(p.precio, 0),
            ancho_bolsa: parseFloatOrDefault(p.ancho_bolsa, 0),
            alto_bolsa: parseFloatOrDefault(p.alto_bolsa, 0),
            fuelle: parseFloatOrDefault(p.fuelle, 0),
            gramaje: parseFloatOrDefault(p.gramaje, 0),
            precio_bobina_kg: parseFloatOrDefault(p.precio_bobina_kg, 0)
        };
    });

    const lineas = formData.lineas.map(l => {
        return {
            sku: l.id,
            nombre: l.nombre,
            capacidad_nominal: parseFloatOrDefault(l.capacidad, 0),
            productos_compatibles: productos.map(p => p.sku)
        };
    });

    const payload = { 
        inversion: {
            objetivo_anr: parseFloatOrDefault(formData.anr, 0),
            fecha_base: formData.fechaBase
        },
        oee_base: {
            disponibilidad: parseFloatOrDefault(formData.dispBase, 0) / 100,
            rendimiento: parseFloatOrDefault(formData.perf, 0) / 100,
            calidad: parseFloatOrDefault(formData.quality, 0) / 100
        },
        catalogo: { productos, lineas }, 
        mix_objetivo: productos.map(p => ({
            producto_id: p.sku,
            porcentaje: productos.length > 0 ? (1.0 / productos.length) : 1.0
        })),
        escenarios: {
            desfavorable: { nombre: 'Desfavorable', tasa_crecimiento_mensual: parseFloatOrDefault(formData.rateDesfavorable, 0) / 100, factor_demanda: 1.0 },
            proyectado: { nombre: 'Proyectado', tasa_crecimiento_mensual: parseFloatOrDefault(formData.rateProyectado, 0) / 100, factor_demanda: 1.0 },
            favorable: { nombre: 'Favorable', tasa_crecimiento_mensual: parseFloatOrDefault(formData.rateFavorable, 0) / 100, factor_demanda: 1.0 }
        },
        capacidad_instalada: {
            capacidad_nominal_por_hora: 2500.0,
            horas_por_turno: 8,
            turnos_por_dia: 1,
            dias_habiles_por_mes: 22,
            dias_inhabiles_mensuales: 1
        },
        ipc: parseFloatOrDefault(formData.ipc, 0) / 100
    };
    
    return payload;
  }
};
