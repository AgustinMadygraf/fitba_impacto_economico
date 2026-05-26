export const SimulationMapper = {
  mapFormToPayload(formData: any) {
    const parseFloatOrDefault = (val: any, def = 0) => {
      const parsed = parseFloat(val);
      return isNaN(parsed) ? def : parsed;
    };

    return {
        inversion: {
            objetivo_anr: parseFloatOrDefault(formData.inversion.objetivo_anr, 0),
            fecha_base: formData.inversion.fecha_base
        },
        oee_base: {
            disponibilidad: parseFloatOrDefault(formData.oee_base.disponibilidad, 0) / 100,
            rendimiento: parseFloatOrDefault(formData.oee_base.rendimiento, 0) / 100,
            calidad: parseFloatOrDefault(formData.oee_base.calidad, 0) / 100
        },
        catalogo: {
            productos: formData.catalogo.productos.map((p: any) => ({
                sku: p.sku,
                nombre: p.nombre,
                precio_unitario: parseFloatOrDefault(p.precio_unitario, 0),
                ancho_bolsa: parseFloatOrDefault(p.ancho_bolsa, 0),
                alto_bolsa: parseFloatOrDefault(p.alto_bolsa, 0),
                fuelle: parseFloatOrDefault(p.fuelle, 0),
                gramaje: parseFloatOrDefault(p.gramaje, 0),
                precio_bobina_kg: parseFloatOrDefault(p.precio_bobina_kg, 0)
            })),
            lineas: formData.catalogo.lineas.map((l: any) => ({
                sku: l.sku,
                nombre: l.nombre,
                capacidad_nominal: parseFloatOrDefault(l.capacidad_nominal, 0),
                productos_compatibles: formData.catalogo.productos.map((p: any) => p.sku)
            }))
        },
        mix_objetivo: formData.catalogo.productos.map((p: any) => ({
            producto_id: p.sku,
            porcentaje: formData.catalogo.productos.length > 0 ? (1.0 / formData.catalogo.productos.length) : 1.0
        })),
        escenarios: {
            desfavorable: { nombre: "Desfavorable", tasa_crecimiento_mensual: parseFloatOrDefault(formData.escenarios.desfavorable, 0) / 100, factor_demanda: 1.0 },
            proyectado: { nombre: "Proyectado", tasa_crecimiento_mensual: parseFloatOrDefault(formData.escenarios.proyectado, 0) / 100, factor_demanda: 1.0 },
            favorable: { nombre: "Favorable", tasa_crecimiento_mensual: parseFloatOrDefault(formData.escenarios.favorable, 0) / 100, factor_demanda: 1.0 }
        },
        capacidad_instalada: formData.capacidad_instalada,
        ipc: parseFloatOrDefault(formData.ipc, 0) / 100
    };
  }
};
