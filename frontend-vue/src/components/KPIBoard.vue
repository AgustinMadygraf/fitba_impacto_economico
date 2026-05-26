<script setup lang="ts">
defineProps<{ resultados: any, realAnr: number }>();
</script>
<template>
  <div class="row g-4 mb-4">
    <div class="col-md-4 text-center border-end border-secondary border-opacity-25">
      <div class="text-muted text-uppercase small">Inversión Actualizada</div>
      <div class="h3 fw-bold text-white mt-1">{{ realAnr }}</div>
    </div>
  </div>
</template>