import React from 'react';
import { motion } from 'framer-motion';

const MetricCard = ({ title, value, unit, icon: Icon, color = 'var(--accent-color)' }) => {
  return (
    <motion.div 
      className="glass-panel"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      style={{ padding: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem' }}
    >
      <div 
        style={{ 
          backgroundColor: `rgba(from ${color} r g b / 0.1)`, 
          padding: '12px', 
          borderRadius: '12px',
          color: color 
        }}
      >
        <Icon size={24} />
      </div>
      <div>
        <h3 style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>{title}</h3>
        <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
          {value} <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>{unit}</span>
        </div>
      </div>
    </motion.div>
  );
};

export default MetricCard;
