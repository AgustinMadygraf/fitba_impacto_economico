import { Logger } from "./logger.js";

export const ApiClient = {
  async post(endpoint, data) {
    Logger.info("API POST request: " + endpoint, { payload: data });
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      if (!response.ok) {
        const errorText = await response.text();
        Logger.error("API POST failed: " + endpoint, { status: response.status, body: errorText });
        throw new Error("HTTP error! status: " + response.status + " " + errorText);
      }
      const result = await response.json();
      Logger.info("API POST success: " + endpoint, { result });
      return result;
    } catch (error) {
      Logger.error("API POST exception: " + endpoint, { error });
      throw error;
    }
  },
  async get(endpoint) {
    Logger.info("API GET request: " + endpoint);
    try {
      const response = await fetch(endpoint);
      if (!response.ok) {
        const errorText = await response.text();
        Logger.error("API GET failed: " + endpoint, { status: response.status, body: errorText });
        throw new Error("HTTP error! status: " + response.status + " " + errorText);
      }
      const result = await response.json();
      Logger.info("API GET success: " + endpoint);
      return result;
    } catch (error) {
      Logger.error("API GET exception: " + endpoint, { error });
      throw error;
    }
  }
};