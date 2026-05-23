/**
 * Responsabilidad: Vincular el estado del DOM con el modelo de datos.
 */
export const FormBinder = {
  getSimulationData() {
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

    return {
      anr: document.getElementById('input-anr').value,
      dispBase: document.getElementById('input-disp-base').value,
      perf: document.getElementById('input-perf').value,
      quality: document.getElementById('input-quality').value,
      productos: productos,
      lineas: lineas,
      rateDesfavorable: document.getElementById('input-rate-desfavorable').value,
      rateProyectado: document.getElementById('input-rate-proyectado').value,
      rateFavorable: document.getElementById('input-rate-favorable').value,
    };
  }
};
