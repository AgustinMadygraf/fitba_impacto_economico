export const Logger = {
  info: (message, context = {}) => console.log("[INFO] " + message, context),
  error: (message, context = {}) => console.error("[ERROR] " + message, context),
  time: (label) => console.time(label),
  timeEnd: (label) => console.timeEnd(label)
};
