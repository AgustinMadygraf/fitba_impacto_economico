import { UINotifier } from './uiNotifier.js';

const generateCorrelationId = () => Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

export const ApiClient = {
    async post(url, data) {
        const correlationId = generateCorrelationId();
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-Correlation-ID': correlationId
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`[CID: ${correlationId}] API Error: ${response.status} - ${JSON.stringify(errorData)}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`[API ERROR CID: ${correlationId}] ${url}:`, error);
            UINotifier.showError(`Error de conexión (ID: ${correlationId}): ${error.message}`);
            throw error;
        }
    }
};
