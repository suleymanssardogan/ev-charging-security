import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldCheck, AlertTriangle, Activity } from 'lucide-react';

const StatusPanel = ({ isAnomaly, anomalyType, confidence = 0.98 }) => {
    return (
        <motion.div
            className="glass-panel"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            style={{ padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1rem', height: '100%' }}
        >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <h3>System Status</h3>
                <Activity size={20} color="var(--text-secondary)" />
            </div>

            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '1rem' }}>
                <AnimatePresence mode="wait">
                    {isAnomaly ? (
                        <motion.div
                            key="anomaly"
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.8, opacity: 0 }}
                            style={{ textAlign: 'center' }}
                        >
                            <div style={{
                                width: '120px', height: '120px', borderRadius: '50%',
                                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                margin: '0 auto 1rem auto',
                                boxShadow: '0 0 40px rgba(239, 68, 68, 0.2)'
                            }}>
                                <AlertTriangle size={64} color="var(--danger-color)" />
                            </div>
                            <h2 style={{ fontSize: '2rem', color: 'var(--danger-color)', marginBottom: '0.5rem' }}>ANOMALY DETECTED</h2>
                            <p style={{ color: 'var(--text-secondary)' }}>Model Confidence: {(confidence * 100).toFixed(1)}%</p>
                            <div style={{ marginTop: '1rem', padding: '0.5rem 1rem', background: 'rgba(239, 68, 68, 0.1)', borderRadius: '8px', color: '#fca5a5' }}>
                                {anomalyType || "Irregular voltage fluctuation"}
                            </div>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="normal"
                            initial={{ scale: 0.8, opacity: 0 }}
                            animate={{ scale: 1, opacity: 1 }}
                            exit={{ scale: 0.8, opacity: 0 }}
                            style={{ textAlign: 'center' }}
                        >
                            <div style={{
                                width: '120px', height: '120px', borderRadius: '50%',
                                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                                margin: '0 auto 1rem auto',
                                boxShadow: '0 0 40px rgba(16, 185, 129, 0.2)'
                            }}>
                                <ShieldCheck size={64} color="var(--success-color)" />
                            </div>
                            <h2 style={{ fontSize: '2rem', color: 'var(--success-color)', marginBottom: '0.5rem' }}>SYSTEM NORMAL</h2>
                            <p style={{ color: 'var(--text-secondary)' }}>Monitoring active session...</p>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>
        </motion.div>
    );
};

export default StatusPanel;
