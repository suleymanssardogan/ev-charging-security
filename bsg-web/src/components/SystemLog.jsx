import React, { useRef, useEffect } from 'react';

const SystemLog = ({ logs }) => {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [logs]);

    return (
        <div className="system-logs">
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem', position: 'sticky', top: 0, background: '#0d1117', paddingBottom: '0.5rem' }}>
                <span style={{ fontWeight: 'bold', color: 'var(--text-secondary)' }}>SYSTEM CONSOLE</span>
                <span style={{ color: 'var(--accent-primary)' }}>RUNNING</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                {logs.map((log, i) => (
                    <div key={i} style={{ display: 'flex', gap: '1rem', opacity: 0.8 }}>
                        <span style={{ color: 'var(--text-muted)', minWidth: '80px' }}>{log.time}</span>
                        <span style={{ color: log.type === 'error' ? 'var(--accent-danger)' : log.type === 'warn' ? 'var(--accent-warning)' : 'var(--text-primary)' }}>
                            {log.type === 'info' && <span style={{ color: 'var(--accent-primary)', marginRight: '8px' }}>[INFO]</span>}
                            {log.type === 'warn' && <span style={{ color: 'var(--accent-warning)', marginRight: '8px' }}>[WARN]</span>}
                            {log.type === 'error' && <span style={{ color: 'var(--accent-danger)', marginRight: '8px' }}>[CRIT]</span>}
                            {log.message}
                        </span>
                    </div>
                ))}
                <div ref={bottomRef} />
            </div>
        </div>
    );
};

export default SystemLog;
