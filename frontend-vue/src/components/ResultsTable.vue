<script setup lang="ts">
defineProps<{ resultados: any[] }>();
</script>
<template>
  <table class="table table-dark table-hover table-borderless align-middle">
    <thead><tr class="text-muted text-uppercase small"><th>Escenario</th><th>Payback</th></tr></thead>
    <tbody>
      <tr v-for="res in resultados" :key="res.escenario">
        <td>{{ res.escenario }}</td>
        <td>{{ res.mes_repago }}</td>
      </tr>
    </tbody>
  </table>
</template>