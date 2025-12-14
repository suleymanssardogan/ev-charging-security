import axios from 'axios';

// Environment variables or defaults (Client-side)
const BILLING_URL = process.env.NEXT_PUBLIC_BILLING_URL || 'http://localhost:9200';
const DETECT_URL = process.env.NEXT_PUBLIC_DETECT_URL || 'http://localhost:9300';
const CP_URL = process.env.NEXT_PUBLIC_CP_URL || 'http://localhost:9400';

export const fetcher = (url) => axios.get(url).then((res) => res.data);

export const api = {
    getInvoices: () => `${BILLING_URL}/invoices`,
    getAlerts: () => `${DETECT_URL}/alerts`,
    runScenario: async (scenario) => {
        return axios.post(`${CP_URL}/start/${scenario}`);
    }
};
