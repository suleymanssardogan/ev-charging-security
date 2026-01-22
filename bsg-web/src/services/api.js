const API_URL = 'http://localhost:8000';

export const fetchSensorData = async () => {
    // Legacy endpoint, kept for compatibility if needed
    try {
        const response = await fetch(`${API_URL}/stream`);
        if (!response.ok) return null;
        return await response.json();
    } catch (error) {
        return null;
    }
};

export const predictMultiFeature = async (featuresList) => {
    try {
        const response = await fetch(`${API_URL}/predict_multifeature`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features: featuresList })
        });
        return await response.json();
    } catch (error) {
        console.error("Prediction failed:", error);
        return { is_anomaly: false, error: "Network Error" };
    }
};
