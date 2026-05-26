<script setup lang="ts">
import { onMounted } from "vue";
onMounted(() => console.log("Navbar montado"));
</script>
<template>
  <nav class="navbar navbar-expand-lg border-bottom border-secondary border-opacity-25 py-3 mb-4">
    <div class="container-fluid px-4">
      <span class="navbar-brand d-flex align-items-center gap-2 text-white">
        <span class="h3 fw-bold mb-0">FITBA</span>
        <span class="badge bg-secondary bg-opacity-25 text-white-50 border border-secondary border-opacity-50">v1.2.2</span>
      </span>
      <span class="text-muted fs-7">Madygraf | Simulador de Impacto</span>
    </div>
  </nav>
</template>