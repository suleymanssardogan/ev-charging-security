import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

const NavItem = ({ href, label }) => {
    const router = useRouter();
    const isActive = router.pathname === href;

    return (
        <Link href={href}>
            <a className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                }`}>
                {/* Icon removed */}
                <span className="font-medium">{label}</span>
            </a>
        </Link>
    );
};

export default function Layout({ children }) {
    return (
        <div className="flex min-h-screen bg-slate-100">
            {/* Sidebar */}
            <aside className="w-64 bg-slate-900 text-white flex flex-col fixed inset-y-0">
                <div className="p-6">
                    <h1 className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
                        OCPP Sentinel
                    </h1>
                    <div className="text-xs text-slate-500 mt-1">Anomaly Detection Lab</div>
                </div>

                <nav className="flex-1 px-4 space-y-1">
                    <NavItem href="/" label="Overview" />
                    <NavItem href="/sessions" label="Sessions" />
                    <NavItem href="/invoices" label="Invoices" />
                    <NavItem href="/alerts" label="Alerts" />
                    <NavItem href="/runner" label="Scenario Runner" />
                    <NavItem href="/settings" label="Settings" />
                </nav>

                <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
                    v1.0.0 Simulation
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 ml-64 p-8 overflow-y-auto">
                {children}
            </main>
        </div>
    );
}
