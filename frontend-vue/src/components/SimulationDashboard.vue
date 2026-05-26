<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { getParametros } from "../api/parametros";
import apiClient from "../api/client";
import Chart from "chart.js/auto";
import ProductList from "./ProductList.vue";
import ProductionLineList from "./ProductionLineList.vue";

const loading = ref(false);
const resultados = ref<any>(null);
const chartRef = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

const form = ref({
   inversion: { objetivo_anr: 0, fecha_base: "" },
   oee_base: { disponibilidad: 0.9, rendimiento: 0.9, calidad: 0.9 },
   catalogo: { productos: [], lineas: [] },
   mix_objetivo: [],
   escenarios: {},
   capacidad_instalada: { capacidad_nominal_por_hora: 1000, horas_por_turno: 8, turnos_por_dia: 1, dias_habiles_por_mes: 20, dias_inhabiles_mensuales: 0 },
   ipc: 0.05
});

onMounted(async () => {
  loading.value = true;
  try {
    const data = await getParametros();
    form.value.inversion = { objetivo_anr: data.inversion.monto_anr_nominal, fecha_base: data.inversion.fecha_base };
    form.value.catalogo = { productos: data.productos, lineas: data.lineas_produccion };
  } finally {
    loading.value = false;
  }
});

onUnmounted(() => { if (chartInstance) chartInstance.destroy(); });

const ejecutarSimulacion = async () => {
  loading.value = true;
  try {
    const response = await apiClient.post("/api/v1/simulacion/ejecutar", form.value);
    resultados.value = response.data;
    renderizarGrafico(resultados.value.proyecciones);
  } catch (error) {
    console.error("Simulation failed:", error);
  } finally {
    loading.value = false;
  }
};

const renderizarGrafico = (proyecciones: any) => {
  if (!chartRef.value) return;
  if (chartInstance) chartInstance.destroy();
  const firstProyeccion = Object.values(proyecciones)[0] as any[];
  if (!firstProyeccion) return;
  const labels = firstProyeccion.map((p: any) => p.fecha);
  const datasets = Object.keys(proyecciones).map((key, i) => ({
    label: key + " (Valor Presente)",
    data: proyecciones[key].map((p: any) => p.beneficio_acumulado_presente),
    borderColor: i === 0 ? "rgba(75, 192, 192, 1)" : "rgba(255, 99, 132, 1)",
    fill: false
  }));
  chartInstance = new Chart(chartRef.value, {
    type: "line",
    data: { labels, datasets },
    options: { responsive: true, maintainAspectRatio: false }
  });
};
</script>

<template>
  <div class="dashboard">
    <h2>Simulación de Impacto</h2>
    <div v-if="loading">Cargando...</div>
    <div v-if="form.inversion">
      <input v-model.number="form.inversion.objetivo_anr" placeholder="ANR Nominal" />
      
      <h3>Productos</h3>
      <ProductList v-model="form.catalogo.productos" />
      
      <h3>Líneas de Producción</h3>
      <ProductionLineList v-model="form.catalogo.lineas" />

      <button @click="ejecutarSimulacion" :disabled="loading">Ejecutar Simulación</button>
      <div v-if="resultados" style="height: 400px; width: 100%;">
        <canvas ref="chartRef"></canvas>
      </div>
    </div>
  </div>
</template>