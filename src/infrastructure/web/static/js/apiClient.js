import { Logger } from "./logger.js";

export const ApiClient = {
  async post(endpoint, data) {
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      if (!response.ok) throw new Error("HTTP error! status: " + response.status);
      return await response.json();
    } catch (error) {
      Logger.error("API POST failed: " + endpoint, { error });
      throw error;
    }
  },
  async get(endpoint) {
    try {
      const response = await fetch(endpoint);
      if (!response.ok) throw new Error("HTTP error! status: " + response.status);
      return await response.json();
    } catch (error) {
      Logger.error("API GET failed: " + endpoint, { error });
      throw error;
    }
  }
};