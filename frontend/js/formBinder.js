/**
 * Responsabilidad: Vincular el estado del DOM con el modelo de datos.
 */
export const FormBinder = {
  getSimulationData() {
    const inputById = document.getElementById('input-vol-base');
    const inputByClass = document.querySelector(".input-linea-capacidad");

    const volBase = inputById?.value || inputByClass?.value;
    
    return {
      anr: document.getElementById('input-anr').value,
      dispBase: document.getElementById('input-disp-base').value,
      perf: document.getElementById('input-perf').value,
      quality: document.getElementById('input-quality').value,
      volBase: parseFloat(volBase) || 0,
      precio: document.getElementById('input-precio').value,
      costo: document.getElementById('input-costo').value,
      rateDesfavorable: document.getElementById('input-rate-desfavorable').value,
      rateProyectado: document.getElementById('input-rate-proyectado').value,
      rateFavorable: document.getElementById('input-rate-favorable').value,
    };
  }
};
