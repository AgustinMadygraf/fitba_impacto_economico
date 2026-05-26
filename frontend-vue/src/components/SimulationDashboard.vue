<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { useSimulation } from "../composables/useSimulation";
import Chart from "chart.js/auto";
import ProductList from "./ProductList.vue";
import ProductionLineList from "./ProductionLineList.vue";
import KPIBoard from "./KPIBoard.vue";
import ResultsTable from "./ResultsTable.vue";

const { form, resultados, loading, cargarParametros, ejecutar } = useSimulation();
const chartRef = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

onMounted(cargarParametros);

watch(resultados, (newRes) => {
  if (newRes?.proyecciones) renderizarGrafico(newRes.proyecciones);
});

const renderizarGrafico = (proyecciones: any) => {
  if (!chartRef.value) return;
  if (chartInstance) chartInstance.destroy();
  const firstKey = Object.keys(proyecciones)[0];
  if (!firstKey) return;
  const firstProyeccion = proyecciones[firstKey] as any[];
  
  const labels = firstProyeccion.map((p: any) => p.fecha);
  const datasets = Object.keys(proyecciones).map((key, i) => ({
    label: key,
    data: proyecciones[key].map((p: any) => p.beneficio_acumulado_presente),
    borderColor: i === 0 ? "cyan" : "magenta"
  }));
  chartInstance = new Chart(chartRef.value, { type: "line", data: { labels, datasets } });
};
</script>

<template>
  <div class="container-fluid px-4">
    <div class="row g-4">
      <aside class="col-lg-4">
        <div class="card p-4">
          <input v-model.number="form.inversion.objetivo_anr" class="form-control mb-2" placeholder="ANR" />
          <ProductList v-model="form.catalogo.productos" />
          <ProductionLineList v-model="form.catalogo.lineas" />
          <button @click="ejecutar" class="btn btn-primary" :disabled="loading">Simular</button>
        </div>
      </aside>
      <main class="col-lg-8">
        <KPIBoard :resultados="resultados" :realAnr="form.inversion.objetivo_anr" />
        <ResultsTable :resultados="resultados?.resultados || []" />
        <canvas ref="chartRef" style="height: 400px; width: 100%;"></canvas>
      </main>
    </div>
  </div>
</template>