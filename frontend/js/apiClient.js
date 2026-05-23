export const ApiClient = {
  async post(endpoint, data) {
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        const errorBody = await response.text();
        console.error(`[API] POST failed: ${endpoint}`, { status: response.status, body: errorBody });
        throw new Error(`API error: ${response.status} - ${errorBody}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`[API] POST exception: ${endpoint}`, { error });
      throw error;
    }
  }
};
