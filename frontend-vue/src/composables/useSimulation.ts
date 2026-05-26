import { ref } from "vue";
import { getParametros } from "../api/parametros";
import { SimulationMapper } from "../services/simulationMapper";
import apiClient from "../api/client";
import type { SimularFormState } from "../types/simulation";

export function useSimulation() {
  const loading = ref(false);
  const resultados = ref<any>(null);
  const form = ref<SimularFormState>({
    inversion: { objetivo_anr: 0, fecha_base: "" },
    oee_base: { disponibilidad: 0, rendimiento: 0, calidad: 0 },
    catalogo: { productos: [], lineas: [] },
    escenarios: { desfavorable: 0, proyectado: 0, favorable: 0 },
    ipc: 0
  });

  const cargarParametros = async () => {
    loading.value = true;
    try {
      const data = await getParametros();
      form.value.inversion = { objetivo_anr: data.inversion.monto_anr_nominal, fecha_base: data.inversion.fecha_base };
      form.value.catalogo = { productos: data.productos, lineas: data.lineas_produccion };
    } finally { loading.value = false; }
  };

  const ejecutar = async () => {
    loading.value = true;
    try {
      const payload = SimulationMapper.mapFormToPayload(form.value);
      const { data } = await apiClient.post("/api/v1/simulacion/ejecutar", payload);
      resultados.value = data;
    } finally { loading.value = false; }
  };

  return { form, resultados, loading, cargarParametros, ejecutar };
}
