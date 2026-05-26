export interface Producto {
  sku: string;
  nombre: string;
  precio_unitario: number;
  costo_marginal_unitario?: number;
}

export interface LineaProduccion {
  sku: string;
  nombre: string;
  capacidad_nominal: number;
}

export interface SimularFormState {
  inversion: { objetivo_anr: number; fecha_base: string };
  oee_base: { disponibilidad: number; rendimiento: number; calidad: number };
  catalogo: { productos: Producto[]; lineas: LineaProduccion[] };
  escenarios: { desfavorable: number; proyectado: number; favorable: number };
  ipc: number;
}
