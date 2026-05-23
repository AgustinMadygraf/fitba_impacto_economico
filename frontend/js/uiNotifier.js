/**
 * Responsabilidad: Notificaciones globales al usuario (Toasts).
 */
export const UINotifier = {
  showError(message) {
    const toastBody = document.getElementById('toast-body');
    if (toastBody) {
        toastBody.textContent = message;
        // eslint-disable-next-line no-undef
        const toast = new bootstrap.Toast(document.getElementById('liveToast'));
        toast.show();
    } else {
        console.error('[FITBA] Error:', message);
        alert(message); // Fallback
    }
  }
};
