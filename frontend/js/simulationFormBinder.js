/**
 * Responsabilidad: Vincular el estado del DOM con el modelo de datos.
 */
export const SimulationFormBinder = {
  getSimulationData() {
    const getVal = (id) => document.getElementById(id)?.value || "0";
    
    // Recolectar Productos
    const productos = Array.from(document.querySelectorAll(".item-producto")).map(div => ({
      id: div.dataset.id,
      nombre: div.querySelector(".input-producto-nombre").value,
      precio: parseFloat(div.querySelector(".input-producto-precio").value) || 0,
      costo: parseFloat(div.querySelector(".input-producto-costo").value) || 0
    }));

    // Recolectar Líneas
    const lineas = Array.from(document.querySelectorAll(".item-linea")).map(div => ({
      id: div.dataset.id,
      nombre: div.querySelector(".input-linea-nombre").value,
      capacidad: parseFloat(div.querySelector(".input-linea-capacidad").value) || 0
    }));

    const data = {
      anr: getVal('input-anr'),
      fechaBase: getVal('input-fecha-base'),
      ipc: getVal('input-ipc'),
      dispBase: getVal('input-disp-base'),
      perf: getVal('input-perf'),
      quality: getVal('input-quality'),
      productos: productos,
      lineas: lineas,
      rateDesfavorable: getVal('input-rate-desfavorable'),
      rateProyectado: getVal('input-rate-proyectado'),
      rateFavorable: getVal('input-rate-favorable'),
    };
    
    return data;
  }
};
