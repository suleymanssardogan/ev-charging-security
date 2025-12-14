import React from 'react';

export default function KpiCard({ title, value, trend, trendValue, color = "blue" }) {
    const colorClasses = {
        blue: "bg-blue-50 text-blue-600",
        red: "bg-red-50 text-red-600",
        green: "bg-green-50 text-green-600",
        purple: "bg-purple-50 text-purple-600",
    };

    return (
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 flex items-start justify-between">
            <div>
                <div className="text-sm font-medium text-slate-500 mb-1">{title}</div>
                <div className="text-3xl font-bold text-slate-900">{value}</div>
                {trend && (
                    <div className={`flex items-center mt-2 text-sm ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
                        <span className="ml-1 font-medium">{trendValue}</span>
                    </div>
                )}
            </div>
            <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
                {/* Icon removed */}
                <span className="text-lg font-bold">#</span>
            </div>
        </div>
    );
}
