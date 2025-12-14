import { useState } from 'react';
import { Play, RotateCw } from 'lucide-react';
import { api } from '../../lib/api';

export default function ScenarioRunnerBar({ onRunComplete }) {
    const [selected, setSelected] = useState('normal');
    const [loading, setLoading] = useState(false);
    const [lastRun, setLastRun] = useState(null);

    const runScenario = async () => {
        setLoading(true);
        try {
            await api.runScenario(selected);
            setLastRun({ id: selected, ts: new Date().toLocaleTimeString() });
            if (onRunComplete) onRunComplete();
        } catch (e) {
            console.error(e);
            alert('Scenario failed: ' + e.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white border-b border-slate-200 p-4 flex items-center justify-between sticky top-0 z-10 shadow-sm">
            <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-slate-600">Scenario:</span>
                    <select
                        value={selected}
                        onChange={(e) => setSelected(e.target.value)}
                        className="bg-slate-50 border border-slate-300 text-slate-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2"
                    >
                        <option value="normal">S0: Normal Session</option>
                        <option value="S1">S1: Monotonicity Violation</option>
                    </select>
                </div>

                <button
                    onClick={runScenario}
                    disabled={loading}
                    className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors disabled:opacity-50 text-sm"
                >
                    <Play size={16} />
                    {loading ? 'Running...' : 'Run Simulation'}
                </button>
            </div>

            <div className="flex items-center gap-4 text-sm">
                {lastRun && (
                    <span className="text-slate-500">
                        Last Run: <span className="font-mono text-slate-700">{lastRun.id}</span> at {lastRun.ts}
                    </span>
                )}
                <button className="text-slate-400 hover:text-slate-600" title="Auto Refresh">
                    <RotateCw size={18} />
                </button>
            </div>
        </div>
    );
}
