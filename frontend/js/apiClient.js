export const ApiClient = {
  async post(endpoint, data) {
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      if (!response.ok) {
        const errorText = await response.text();
        if (window.APP_CONFIG && window.APP_CONFIG.mode === 'development') console.error("API POST failed: " + endpoint, { status: response.status, body: errorText });
        throw new Error("HTTP error! status: " + response.status + " " + errorText);
      }
      const result = await response.json();
      return result;
    } catch (error) {
      if (window.APP_CONFIG && window.APP_CONFIG.mode === 'development') console.error("API POST exception: " + endpoint, { error });
      throw error;
    }
  },
  async get(endpoint) {
    try {
      const response = await fetch(endpoint);
      if (!response.ok) {
        const errorText = await response.text();
        if (window.APP_CONFIG && window.APP_CONFIG.mode === 'development') console.error("API GET failed: " + endpoint, { status: response.status, body: errorText });
        throw new Error("HTTP error! status: " + response.status + " " + errorText);
      }
      const result = await response.json();
      return result;
    } catch (error) {
      if (window.APP_CONFIG && window.APP_CONFIG.mode === 'development') console.error("API GET exception: " + endpoint, { error });
      throw error;
    }
  }
};
