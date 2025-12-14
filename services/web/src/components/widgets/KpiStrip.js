import { DollarSign, Zap, AlertTriangle, Activity } from 'lucide-react';

const KpiItem = ({ label, value, subtext, icon: Icon, color }) => (
    <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center justify-between shadow-sm">
        <div>
            <p className="text-xs font-medium text-slate-500 uppercase tracking-wider">{label}</p>
            <p className="text-2xl font-bold text-slate-900 mt-1">{value}</p>
            {subtext && <p className="text-xs text-slate-400 mt-1">{subtext}</p>}
        </div>
        <div className={`p-3 rounded-lg bg-${color}-50 text-${color}-600`}>
            <Icon size={24} />
        </div>
    </div>
);

export default function KpiStrip({ totalCost, totalKwh, activeAlerts, sessionCount }) {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <KpiItem
                label="Total Cost"
                value={`$${totalCost}`}
                icon={DollarSign}
                color="green"
            />
            <KpiItem
                label="Total Energy"
                value={`${totalKwh} kWh`}
                icon={Zap}
                color="blue"
            />
            <KpiItem
                label="Active Alerts"
                value={activeAlerts}
                subtext="High Severity"
                icon={AlertTriangle}
                color="red"
            />
            <KpiItem
                label="Total Sessions"
                value={sessionCount}
                icon={Activity}
                color="purple"
            />
        </div>
    );
}
