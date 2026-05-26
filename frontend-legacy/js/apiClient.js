import { UINotifier } from './uiNotifier.js';

const generateCorrelationId = () => Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);

export const ApiClient = {
    async post(url, data) {
        const correlationId = generateCorrelationId();
        // console.log(`[API REQUEST CID: ${correlationId}] POST ${url}`, data);
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
                console.warn(`[API WARNING CID: ${correlationId}] ${url} returned ${response.status}`, errorData);
                throw new Error(`[CID: ${correlationId}] API Error: ${response.status} - ${JSON.stringify(errorData)}`);
            }
            const result = await response.json();
            // console.log(`[API RESPONSE CID: ${correlationId}] ${url} success`);
            return result;
        } catch (error) {
            console.error(`[API ERROR CID: ${correlationId}] ${url}:`, error);
            UINotifier.showError(`Error de conexión (ID: ${correlationId}): ${error.message}`);
            throw error;
        }
    }
};
