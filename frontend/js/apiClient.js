export const ApiClient = {
  async post(endpoint, data) {
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
      const errorText = await response.text();
      if (!response.ok) {
        console.error("API POST failed: " + endpoint, { status: response.status, body: errorText });
        throw new Error("API error: " + response.status + " - " + errorText);
      }
      return JSON.parse(errorText || "{}");
    } catch (error) {
      console.error("API POST exception: " + endpoint, { error });
      throw error;
    }
  },
  async get(endpoint) {
    try {
      const response = await fetch(endpoint);
      const errorText = await response.text();
      if (!response.ok) {
        console.error("API GET failed: " + endpoint, { status: response.status, body: errorText });
        throw new Error("API error: " + response.status + " - " + errorText);
      }
      return JSON.parse(errorText || "{}");
    } catch (error) {
      console.error("API GET exception: " + endpoint, { error });
      throw error;
    }
  }
};
