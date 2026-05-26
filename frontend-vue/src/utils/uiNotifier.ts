export const UINotifier = {
  showError(message: string) { alert("Error: " + message); },
  showInfo(message: string) { console.info(message); },
  showSuccess(message: string) { console.info(message); },
  showWarning(message: string) { console.warn(message); }
};
