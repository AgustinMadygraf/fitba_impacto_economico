<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getParametros } from './api/parametros';

const data = ref(null);
const error = ref(null);

onMounted(async () => {
  try {
    data.value = await getParametros();
  } catch (e: any) {
    error.value = e.message;
  }
});
</script>

<template>
  <div id="app">
    <h1>FITBA Impacto Económico</h1>
    <div v-if="error">Error: {{ error }}</div>
    <pre v-if="data">{{ data }}</pre>
  </div>
</template>
