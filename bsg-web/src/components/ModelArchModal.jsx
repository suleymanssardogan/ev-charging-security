import React, { useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Cpu, X, GitBranch, Box, Layers, Zap } from 'lucide-react';

const ModelArchModal = ({ isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                style={{
                    position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
                    background: 'rgba(0,0,0,0.8)', zIndex: 9999,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    backdropFilter: 'blur(8px)'
                }}
                onClick={onClose}
            >
                <motion.div
                    initial={{ scale: 0.9, y: 20 }}
                    animate={{ scale: 1, y: 0 }}
                    exit={{ scale: 0.9, y: 20 }}
                    style={{
                        background: '#0d1117',
                        border: '1px solid var(--border-color)',
                        borderRadius: '16px',
                        width: '600px',
                        maxWidth: '90vw',
                        overflow: 'hidden',
                        boxShadow: '0 20px 50px rgba(0,0,0,0.5)'
                    }}
                    onClick={(e) => e.stopPropagation()}
                >
                    {/* Header */}
                    <div style={{ padding: '1.5rem', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                            <div style={{ padding: '0.5rem', background: 'rgba(47, 129, 247, 0.15)', borderRadius: '8px', color: 'var(--accent-primary)' }}>
                                <Cpu size={24} />
                            </div>
                            <div>
                                <h2 style={{ fontSize: '1.25rem', color: 'var(--text-primary)' }}>Model Architecture</h2>
                                <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Technical Specification</p>
                            </div>
                        </div>
                        <button onClick={onClose} style={{ color: 'var(--text-secondary)', padding: '0.5rem', cursor: 'pointer', borderRadius: '50%' }}>
                            <X size={20} />
                        </button>
                    </div>

                    {/* Content */}
                    <div style={{ padding: '2rem' }}>
                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
                            <ConfigItem
                                icon={<GitBranch size={20} />}
                                label="Algorithm"
                                value="Random Forest Classifier"
                                color="#a371f7"
                            />
                            <ConfigItem
                                icon={<Layers size={20} />}
                                label="Ensemble Size"
                                value="50 Estimators (Trees)"
                                color="#2f81f7"
                            />
                            <ConfigItem
                                icon={<Box size={20} />}
                                label="Input Dimension"
                                value="12 Features"
                                color="#2ea043"
                            />
                            <ConfigItem
                                icon={<Zap size={20} />}
                                label="Output Classes"
                                value="11 Categories"
                                color="#f85149"
                            />
                        </div>

                        {/* Architecture Visualization (Abstract) */}
                        <div style={{ background: '#161b22', padding: '1rem', borderRadius: '12px' }}>
                            <div style={{ fontSize: '0.8rem', fontWeight: 'bold', color: 'var(--text-muted)', marginBottom: '1rem', textTransform: 'uppercase' }}>Pipeline Visualization</div>
                            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem', overflowX: 'auto' }}>
                                <Node label="Raw Data" sub="Can Bus" />
                                <Arrow />
                                <Node label="Preprocessing" sub="Scaling" />
                                <Arrow />
                                <Node label="Feature Eng" sub="Calculated" />
                                <Arrow />
                                <Node label="Random Forest" sub="50 Trees" active />
                                <Arrow />
                                <Node label="Classification" sub="11 Classes" />
                            </div>
                        </div>
                    </div>

                    {/* Footer */}
                    <div style={{ padding: '1rem 1.5rem', background: '#161b22', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'flex-end' }}>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                            Framework: <strong>Scikit-Learn v1.6.1</strong>
                        </div>
                    </div>
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
};

const ConfigItem = ({ icon, label, value, color }) => (
    <div style={{ display: 'flex', alignItems: 'start', gap: '1rem' }}>
        <div style={{ marginTop: '2px', color: color }}>{icon}</div>
        <div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '2px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{label}</div>
            <div style={{ fontSize: '1rem', fontWeight: '600', color: 'var(--text-primary)' }}>{value}</div>
        </div>
    </div>
);

const Node = ({ label, sub, active }) => (
    <div style={{
        background: active ? 'rgba(47, 129, 247, 0.1)' : '#0d1117',
        border: `1px solid ${active ? 'var(--accent-primary)' : 'var(--border-color)'}`,
        padding: '0.75rem', borderRadius: '8px', minWidth: '100px', textAlign: 'center'
    }}>
        <div style={{ fontSize: '0.8rem', fontWeight: '600', color: active ? 'var(--accent-primary)' : 'var(--text-primary)' }}>{label}</div>
        <div style={{ fontSize: '0.7rem', color: 'var(--text-secondary)' }}>{sub}</div>
    </div>
);

const Arrow = () => (
    <div style={{ color: 'var(--text-muted)' }}>→</div>
);

export default ModelArchModal;
