<script setup lang="ts">
const props = defineProps<{ modelValue: any[] }>();
const emit = defineEmits(["update:modelValue"]);

const updateProduct = (index: number, key: string, value: any) => {
  const products = [...props.modelValue];
  products[index][key] = value;
  emit("update:modelValue", products);
};

const addProduct = () => {
  const products = [...props.modelValue, { sku: "NEW-" + Date.now(), nombre: "", precio_unitario: 0, costo: 0 }];
  emit("update:modelValue", products);
};

const removeProduct = (index: number) => {
  const products = props.modelValue.filter((_, i) => i !== index);
  emit("update:modelValue", products);
};
</script>

<template>
  <div v-for="(prod, index) in props.modelValue" :key="prod.sku" class="card mb-2 p-2 bg-dark bg-opacity-10">
    <input :value="prod.nombre" @input="updateProduct(index, 'nombre', ($event.target as HTMLInputElement).value)" class="form-control mb-1" placeholder="Nombre" />
    <div class="d-flex gap-2">
      <input type="number" :value="prod.precio_unitario" @input="updateProduct(index, 'precio_unitario', parseFloat(($event.target as HTMLInputElement).value))" class="form-control" placeholder="Precio" />
      <button @click="removeProduct(index)" class="btn btn-sm btn-danger">X</button>
    </div>
  </div>
  <button @click="addProduct" class="btn btn-sm btn-outline-secondary w-100">+ Agregar Producto</button>
</template>
