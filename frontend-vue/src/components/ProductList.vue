<script setup lang="ts">
const props = defineProps<{ modelValue: any[] }>();
const emit = defineEmits(["update:modelValue"]);

const updateProduct = (index: number, key: string, value: any) => {
  const products = [...props.modelValue];
  products[index][key] = value;
  emit("update:modelValue", products);
};
</script>

<template>
  <div v-for="(prod, index) in props.modelValue" :key="prod.sku" class="mb-2">
    <input :value="prod.nombre" @input="updateProduct(index, 'nombre', ($event.target as HTMLInputElement).value)" placeholder="Nombre" />
    <input type="number" :value="prod.precio_unitario" @input="updateProduct(index, 'precio_unitario', parseFloat(($event.target as HTMLInputElement).value))" placeholder="Precio" />
  </div>
</template>
