/*
Path: src/infrastructure/web/static/js/logger.js
*/

// Se inicializa con un valor por defecto seguro (producción)
window.APP_CONFIG = { mode: 'production' };

// Cargar configuración desde el backend
fetch('/api/config')
  .then(response => response.json())
  .then(config => {
    window.APP_CONFIG = config;
    console.log("Configuración cargada:", window.APP_CONFIG);
  })
  .catch(err => console.error("Error cargando configuración:", err));

export const Logger = {
  info: (message, context = {}) => {
    if (window.APP_CONFIG.mode === 'development') {
      console.log("[INFO] " + message, context);
    }
  },
  error: (message, context = {}) => {
    if (window.APP_CONFIG.mode === 'development') {
      console.error("[ERROR] " + message, context);
    }
  },
  time: (label) => {
    if (window.APP_CONFIG.mode === 'development') {
      console.time(label);
    }
  },
  timeEnd: (label) => {
    if (window.APP_CONFIG.mode === 'development') {
      console.timeEnd(label);
    }
  }
};
