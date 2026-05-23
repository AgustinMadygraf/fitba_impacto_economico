export const Logger = {
  info: (message, context = {}) => console.log("[INFO] " + message, context),
  error: (message, context = {}) => console.error("[ERROR] " + message, context)
};