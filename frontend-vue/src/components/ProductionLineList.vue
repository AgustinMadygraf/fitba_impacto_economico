<script setup lang="ts">
const props = defineProps<{ modelValue: any[] }>();
const emit = defineEmits(["update:modelValue"]);

const updateLine = (index: number, key: string, value: any) => {
  const lines = [...props.modelValue];
  lines[index][key] = value;
  emit("update:modelValue", lines);
};

const addLine = () => {
  const lines = [...props.modelValue, { sku: "LINE-" + Date.now(), nombre: "", capacidad_nominal: 0 }];
  emit("update:modelValue", lines);
};

const removeLine = (index: number) => {
  const lines = props.modelValue.filter((_, i) => i !== index);
  emit("update:modelValue", lines);
};
</script>

<template>
  <div v-for="(line, index) in props.modelValue" :key="line.sku" class="card mb-2 p-2 bg-dark bg-opacity-10">
    <input :value="line.nombre" @input="updateLine(index, 'nombre', ($event.target as HTMLInputElement).value)" class="form-control mb-1" placeholder="Nombre" />
    <div class="d-flex gap-2">
      <input type="number" :value="line.capacidad_nominal" @input="updateLine(index, 'capacidad_nominal', parseFloat(($event.target as HTMLInputElement).value))" class="form-control" placeholder="Capacidad" />
      <button @click="removeLine(index)" class="btn btn-sm btn-danger">X</button>
    </div>
  </div>
  <button @click="addLine" class="btn btn-sm btn-outline-secondary w-100">+ Agregar Línea</button>
</template>
