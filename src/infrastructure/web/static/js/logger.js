/*
Path: src/infrastructure/web/static/js/logger.js
*/

// Inicializar antes de la petición para evitar undefined
window.APP_CONFIG = { mode: 'production' };

window.CONFIG_LOADED = fetch('/api/config')
  .then(response => response.json())
  .then(config => {
    window.APP_CONFIG = config;
    return config;
  })
  .catch(err => {
    console.error("Error cargando configuración:", err);
    return window.APP_CONFIG;
  });
