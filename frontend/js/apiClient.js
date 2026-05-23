import { UINotifier } from './uiNotifier.js';

export const ApiClient = {
    async post(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`API Error: ${response.status} - ${JSON.stringify(errorData)}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`[API ERROR] ${url}:`, error);
            UINotifier.showError(`Error de conexión: ${error.message}`);
            throw error;
        }
    }
};
