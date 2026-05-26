/**
 * Responsabilidad: Notificaciones globales al usuario (Toasts).
 */
export const UINotifier = {
  showError(message) {
    this._show(message, 'danger');
  },
  showInfo(message) {
    this._show(message, 'info');
  },
  showSuccess(message) {
    this._show(message, 'success');
  },
  showWarning(message) {
    this._show(message, 'warning');
    console.warn('[FITBA] Warning:', message);
  },
  _show(message, type) {
    const toastBody = document.getElementById('toast-body');
    const toastElement = document.getElementById('liveToast');
    if (toastBody && toastElement) {
        toastBody.textContent = message;
        toastElement.className = `toast align-items-center text-white bg-${type} border-0`;
        // eslint-disable-next-line no-undef
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    } else {
        console.log(`[FITBA] ${type.toUpperCase()}:`, message);
        alert(message); // Fallback
    }
  }
};
