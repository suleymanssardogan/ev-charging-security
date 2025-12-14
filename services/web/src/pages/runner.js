import { useState } from 'react';
import Layout from '../components/layout/Layout';
import { api } from '../lib/api';

const ScenarioCard = ({ id, name, description, active, onClick }) => (
    <div
        onClick={onClick}
        className={`p-6 rounded-xl border cursor-pointer transition-all ${active
                ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-200'
                : 'border-slate-200 bg-white hover:border-blue-300'
            }`}
    >
        <div className="flex justify-between items-start">
            <h3 className="font-bold text-slate-900">{name}</h3>
            <span className="text-xs font-mono bg-slate-100 px-2 py-1 rounded">{id}</span>
        </div>
        <p className="text-sm text-slate-500 mt-2">{description}</p>
    </div>
);

export default function Runner() {
    const [selected, setSelected] = useState('normal');
    const [loading, setLoading] = useState(false);
    const [status, setStatus] = useState(null);

    const runScenario = async () => {
        setLoading(true);
        setStatus(null);
        try {
            await api.runScenario(selected);
            setStatus({ type: 'success', msg: `Scenario ${selected} started successfully.` });
        } catch (e) {
            setStatus({ type: 'error', msg: `Failed to start scenario: ${e.message}` });
        } finally {
            setLoading(false);
        }
    };

    const scenarios = [
        { id: 'normal', name: 'Normal Session', description: 'Standard charging session with no anomalies. Baseline test (S0).' },
        { id: 'S1', name: 'Monotonicity Violation', description: 'Meter values decrease during transaction (K1).' },
    ];

    return (
        <Layout>
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-slate-900">Scenario Runner</h1>
                <p className="text-slate-500">Trigger simulation scenarios to test detection rules.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {scenarios.map(s => (
                    <ScenarioCard
                        key={s.id}
                        {...s}
                        active={selected === s.id}
                        onClick={() => setSelected(s.id)}
                    />
                ))}
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm max-w-2xl">
                <div className="flex items-center justify-between">
                    <div>
                        <h3 className="font-medium text-slate-900">Ready to Launch</h3>
                        <p className="text-sm text-slate-500">Selected: <span className="font-bold font-mono">{selected}</span></p>
                    </div>
                    <button
                        onClick={runScenario}
                        disabled={loading}
                        className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors disabled:opacity-50"
                    >
                        {loading ? 'Starting...' : 'Run Scenario'}
                    </button>
                </div>

                {status && (
                    <div className={`mt-4 p-4 rounded-lg flex items-center gap-2 ${status.type === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
                        {status.msg}
                    </div>
                )}
            </div>
        </Layout>
    );
}
