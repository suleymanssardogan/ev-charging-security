import React, { useState, useEffect, useRef } from 'react';
import MetricCard from './MetricCard';
import LiveChart from './LiveChart';
import StatusPanel from './StatusPanel';
import SystemLog from './SystemLog';
import { predictMultiFeature } from '../services/api';
import Papa from 'papaparse';
import {
    Zap, Activity, Thermometer, Battery,
    Play, Pause, RefreshCw, Upload,
    LayoutDashboard, FileText, Settings, ShieldAlert, Cpu
} from 'lucide-react';

import ModelArchModal from './ModelArchModal';

const Dashboard = () => {
    // --- State ---
    const [data, setData] = useState([]);
    const [logs, setLogs] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);

    // Core Metrics
    const [metrics, setMetrics] = useState({ v: 0, i: 0, t: 0, s: 0 });
    const [systemStatus, setSystemStatus] = useState({ isAnomaly: false, type: null, confidence: 0, solution: null });

    // Simulation State
    const [scenario, setScenario] = useState("live");
    const [isPlaying, setIsPlaying] = useState(false);
    const [simData, setSimData] = useState([]);
    const [simIndex, setSimIndex] = useState(0);
    const timerRef = useRef(null);

    // Logging Helper
    const addLog = (message, type = 'info') => {
        const now = new Date().toLocaleTimeString().split(' ')[0] + '.' + new Date().getMilliseconds();
        setLogs(prev => [...prev.slice(-49), { time: now, message, type }]);
    };

    // --- Simulation Loop ---
    useEffect(() => {
        if (isPlaying && (scenario === 'csv_replay')) {
            timerRef.current = setInterval(() => {
                setSimIndex(prev => {
                    if (prev >= simData.length) {
                        setIsPlaying(false);
                        addLog("Simulation completed.", "info");
                        return prev;
                    }

                    const row = simData[prev]; // Array of values
                    processFrame(row);
                    return prev + 1;
                });
            }, 800);
        }
        return () => clearInterval(timerRef.current);
    }, [isPlaying, simData, scenario]);

    // Data Processing
    const processFrame = (features) => {
        // IMPORTANT: We need to match the 12 columns the model expects.
        // If the CSV has 20 columns, we might need to take the first 12, or specific indices.
        // Assuming the first 12 are the correct features for now.
        const modelInput = features.slice(0, 12);

        // 1. Update Metrics (Assuming generic first few columns correspond to physical values for visualization)
        // Adjust these indices based on real column mapping of the 12 features
        // Example: Voltage might be index 3, Current index 4 based on your 'check_viz.txt' output
        // Index(['latency_ms', 'integrity_flag', 'token_visible', 'voltage_v', 'current_a', 'temperature_c' ...])
        const newMetrics = {
            v: features[3] || 0,
            i: features[4] || 0,
            t: features[5] || 0,
            s: features[6] || 0 // 'meter_kwh' as proxy for activity?
        };
        setMetrics(newMetrics);

        // 2. Predict (Call backend)
        predictMultiFeature(modelInput).then(res => {
            if (res.is_anomaly) {
                setSystemStatus({
                    isAnomaly: true,
                    type: res.type,
                    solution: res.solution,
                    confidence: res.confidence || 0.98
                });

                // Log only if it's a new error or periodic
                addLog(`⚠️ ${res.type} (${(res.confidence * 100).toFixed(1)}%): ${res.solution.split('\n')[0]}`, "error");
            } else {
                // If backend returns high confidence for NORMAL, use it. 
                // Otherwise default to high confidence for normal state.
                const conf = res.confidence > 0.1 ? res.confidence : 0.99;
                setSystemStatus({ isAnomaly: false, type: "NORMAL", solution: null, confidence: conf });
            }
        });

        // 3. Update Chart
        setData(prev => {
            const next = [...prev, {
                time: new Date().toLocaleTimeString(),
                voltage: newMetrics.v,
                temp: newMetrics.t
            }];
            if (next.length > 40) next.shift();
            return next;
        });
    };

    // CSV Upload Support
    const handleFileUpload = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        Papa.parse(file, {
            header: false, // We parse as arrays to be generic
            dynamicTyping: true,
            skipEmptyLines: true,
            complete: (res) => {
                let rawData = res.data;

                // DATA CLEANING: Remove Header if present
                // Check if the first column of the first row is a String (header) instead of a Number
                if (rawData.length > 0 && typeof rawData[0][0] === 'string') {
                    // Double check it's not just a weird number string
                    if (isNaN(parseFloat(rawData[0][0]))) {
                        rawData = rawData.slice(1);
                        addLog("Removed CSV header row automatically.", "info");
                    }
                }

                // Filter for valid numeric rows (at least 12 columns)
                const cleanData = rawData.filter(row => {
                    // Check length and ensure at least the first value is numeric-ish
                    return row.length >= 12 && !isNaN(row[0]);
                });

                if (cleanData.length > 0) {
                    setSimData(cleanData);
                    setScenario('csv_replay');
                    setSimIndex(0);
                    setIsPlaying(true);
                    addLog(`Loaded external CSV: ${file.name} (${cleanData.length} samples)`, "info");
                } else {
                    addLog("Error: No valid numeric data found in CSV.", "error");
                }
            },
            error: (err) => {
                addLog(`CSV Parse Error: ${err.message}`, "error");
            }
        });
    };

    return (
        <div className="app-layout">
            {/* SIDEBAR */}
            <aside className="sidebar">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border-color)' }}>
                    <div style={{ width: '32px', height: '32px', background: 'var(--accent-primary)', borderRadius: '6px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <ShieldAlert color="white" size={20} />
                    </div>
                    <div>
                        <div style={{ fontWeight: 'bold', fontSize: '1rem' }}>EV Security Architecture</div>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>v1.0.0-final</div>
                    </div>
                </div>

                <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    <div style={{ paddingLeft: '0.5rem', fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--text-muted)', marginBottom: '0.25rem' }}>DASHBOARD</div>
                    <button className={`tech-btn ${scenario === 'live' ? 'active' : ''}`} onClick={() => { setScenario('live'); setIsPlaying(false); }}>
                        <Activity size={16} /> Live Monitor
                    </button>

                    <div style={{ paddingLeft: '0.5rem', fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--text-muted)', marginBottom: '0.25rem', marginTop: '1rem' }}>SIMULATION SCENARIOS</div>

                    <label className={`tech-btn ${scenario === 'csv_replay' ? 'active' : ''}`} style={{ cursor: 'pointer' }}>
                        <FileText size={16} /> Load Test Data (CSV)
                        <input type="file" style={{ display: 'none' }} accept=".csv" onChange={handleFileUpload} />
                    </label>

                    <div style={{ paddingLeft: '0.5rem', fontSize: '0.75rem', fontWeight: 'bold', color: 'var(--text-muted)', marginBottom: '0.25rem', marginTop: '1rem' }}>SYSTEM</div>
                    {/* Model Config Removed */}

                    <button className="tech-btn" onClick={() => setIsModalOpen(true)}>
                        <Cpu size={16} /> Model Architecture
                    </button>
                </nav>
            </aside>

            {/* HEADER */}
            <header className="header">
                <h2 style={{ fontSize: '1.25rem', fontWeight: '500' }}>
                    {scenario === 'live' ? 'Real-Time Threat Detection' : 'Scenario Analysis Mode'}
                </h2>

                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                    {scenario !== 'live' && (
                        <div style={{ display: 'flex', gap: '0.5rem', marginRight: '1rem' }}>
                            <button className="tech-btn" onClick={() => setIsPlaying(!isPlaying)}>
                                {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                                {isPlaying ? 'Pause' : 'Resume'}
                            </button>
                            <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', alignSelf: 'center' }}>
                                Frame: {simIndex} / {simData.length}
                            </span>
                        </div>
                    )}

                    <div className={`status-badge ${systemStatus.isAnomaly ? 'anomaly' : 'normal'}`}>
                        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'currentColor' }}></div>
                        {systemStatus.isAnomaly ? 'THREAT DETECTED' : 'SYSTEM SECURE'}
                    </div>
                </div>
            </header>

            {/* MAIN CONTENT */}
            <main className="main-content">
                {/* Metrics */}
                <div className="metric-grid">
                    <MetricCard title="Voltage (V)" value={metrics.v.toFixed(1)} unit="V" icon={Zap} color="var(--accent-warning)" />
                    <MetricCard title="Current (A)" value={metrics.i.toFixed(1)} unit="A" icon={Activity} color="var(--accent-primary)" />
                    <MetricCard title="Temperature" value={metrics.t.toFixed(1)} unit="°C" icon={Thermometer} color="var(--accent-danger)" />
                    <MetricCard title="Meter Value" value={metrics.s.toFixed(1)} unit="kWh" icon={Battery} color="var(--accent-success)" />
                </div>

                {/* Grid */}
                <div className="chart-grid">
                    <div className="flex flex-col gap-4">
                        <LiveChart title="Voltage Frequency Domain" data={data} dataKey="voltage" color="var(--accent-warning)" />
                        <LiveChart title="Thermal Signature" data={data} dataKey="temp" color="var(--accent-danger)" />
                    </div>

                    <div className="flex flex-col gap-4">
                        <StatusPanel isAnomaly={systemStatus.isAnomaly} anomalyType={systemStatus.type} confidence={systemStatus.confidence} />

                        {/* Model Insight Box */}
                        <div className="tech-card" style={{ padding: '1.5rem', flex: 1, overflow: 'auto' }}>
                            <h3 style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem' }}>AI ANALYSIS</h3>

                            {systemStatus.isAnomaly && systemStatus.solution ? (
                                <div style={{ fontSize: '0.85rem', color: '#e6edf3' }}>
                                    <div style={{ marginBottom: '1rem', paddingBottom: '0.5rem', borderBottom: '1px solid var(--border-color)' }}>
                                        <strong>Root Cause:</strong> {systemStatus.type}
                                    </div>
                                    <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.5' }}>
                                        {systemStatus.solution}
                                    </div>
                                </div>
                            ) : (
                                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                                    System operating within normal parameters.
                                </div>
                            )}

                            <div style={{ marginTop: 'auto', paddingTop: '1rem', display: 'flex', justifyContent: 'space-between', borderTop: '1px solid var(--border-color)' }}>
                                <span style={{ color: 'var(--text-muted)' }}>Confidence</span>
                                <span style={{ color: systemStatus.isAnomaly ? 'var(--accent-danger)' : 'var(--accent-success)' }}>
                                    {(systemStatus.confidence * 100).toFixed(1)}%
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* LOGS */}
            <SystemLog logs={logs} />

            {/* MODALS */}
            <ModelArchModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
        </div>
    );
};

export default Dashboard;
