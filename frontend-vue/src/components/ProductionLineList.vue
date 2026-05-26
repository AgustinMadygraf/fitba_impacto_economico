<script setup lang="ts">
const props = defineProps<{ modelValue: any[] }>();
const emit = defineEmits(["update:modelValue"]);

const updateLine = (index: number, key: string, value: any) => {
  const lines = [...props.modelValue];
  lines[index][key] = value;
  emit("update:modelValue", lines);
};
</script>

<template>
  <div v-for="(line, index) in props.modelValue" :key="line.sku" class="mb-2">
    <input :value="line.nombre" @input="updateLine(index, 'nombre', ($event.target as HTMLInputElement).value)" placeholder="Nombre" />
    <input type="number" :value="line.capacidad_nominal" @input="updateLine(index, 'capacidad_nominal', parseFloat(($event.target as HTMLInputElement).value))" placeholder="Capacidad" />
  </div>
</template>
