import { useState } from 'react';
import * as Tabs from '@radix-ui/react-tabs';
import { FileText, AlertTriangle, Zap } from 'lucide-react';
import Badge from '../Badge';

const TableRow = ({ children, onClick }) => (
    <tr onClick={onClick} className="hover:bg-blue-50 cursor-pointer transition-colors border-b border-slate-50 last:border-0">
        {children}
    </tr>
);

const Cell = ({ children, className }) => (
    <td className={`px-6 py-4 text-sm ${className}`}>{children}</td>
);

export default function MasterGrid({ sessions, invoices, alerts, onRowClick }) {
    return (
        <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-[500px]">
            <Tabs.Root defaultValue="sessions" className="flex flex-col h-full">
                <div className="border-b border-slate-200 px-6 pt-4 bg-slate-50">
                    <Tabs.List className="flex gap-6">
                        <Tabs.Trigger value="sessions" className="pb-3 border-b-2 border-transparent data-[state=active]:border-blue-600 data-[state=active]:text-blue-600 text-slate-500 font-medium text-sm flex items-center gap-2 outline-none">
                            <Zap size={16} /> Sessions
                        </Tabs.Trigger>
                        <Tabs.Trigger value="invoices" className="pb-3 border-b-2 border-transparent data-[state=active]:border-blue-600 data-[state=active]:text-blue-600 text-slate-500 font-medium text-sm flex items-center gap-2 outline-none">
                            <FileText size={16} /> Invoices
                        </Tabs.Trigger>
                        <Tabs.Trigger value="alerts" className="pb-3 border-b-2 border-transparent data-[state=active]:border-blue-600 data-[state=active]:text-blue-600 text-slate-500 font-medium text-sm flex items-center gap-2 outline-none">
                            <AlertTriangle size={16} /> Alerts
                            {alerts?.length > 0 && <span className="bg-red-100 text-red-600 text-xs px-2 rounded-full ml-1">{alerts.length}</span>}
                        </Tabs.Trigger>
                    </Tabs.List>
                </div>

                <div className="flex-1 overflow-auto">
                    <Tabs.Content value="sessions" className="h-full">
                        <table className="w-full text-left">
                            <thead className="bg-white sticky top-0 z-10 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                                <tr>
                                    <th className="px-6 py-3">Tx ID</th>
                                    <th className="px-6 py-3">Station</th>
                                    <th className="px-6 py-3">Total kWh</th>
                                    <th className="px-6 py-3">Duration</th>
                                    <th className="px-6 py-3">Cost</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {sessions?.map(s => (
                                    <TableRow key={s.transactionId} onClick={() => onRowClick('session', s)}>
                                        <Cell><span className="font-mono text-slate-600">#{s.transactionId}</span></Cell>
                                        <Cell>{s.chargePointId}</Cell>
                                        <Cell>{s.totalKwh}</Cell>
                                        <Cell>-</Cell>
                                        <Cell className="font-bold text-slate-700">${s.totalCost?.toFixed(2)}</Cell>
                                    </TableRow>
                                ))}
                            </tbody>
                        </table>
                    </Tabs.Content>

                    <Tabs.Content value="invoices" className="h-full">
                        <table className="w-full text-left">
                            <thead className="bg-white sticky top-0 z-10 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                                <tr>
                                    <th className="px-6 py-3">Invoice ID</th>
                                    <th className="px-6 py-3">Tx ID</th>
                                    <th className="px-6 py-3">Total Cost</th>
                                    <th className="px-6 py-3">Status</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {invoices?.map(i => (
                                    <TableRow key={i.transactionId} onClick={() => onRowClick('invoice', i)}>
                                        <Cell><span className="font-mono text-slate-600">INV-{i.transactionId}</span></Cell>
                                        <Cell><span className="font-mono">#{i.transactionId}</span></Cell>
                                        <Cell className="font-bold text-slate-700">${i.totalCost?.toFixed(2)}</Cell>
                                        <Cell><Badge variant="success">GENERATED</Badge></Cell>
                                    </TableRow>
                                ))}
                            </tbody>
                        </table>
                    </Tabs.Content>

                    <Tabs.Content value="alerts" className="h-full">
                        <table className="w-full text-left">
                            <thead className="bg-white sticky top-0 z-10 text-xs font-semibold text-slate-500 uppercase tracking-wider border-b border-slate-200">
                                <tr>
                                    <th className="px-6 py-3">Time</th>
                                    <th className="px-6 py-3">Rule</th>
                                    <th className="px-6 py-3">Severity</th>
                                    <th className="px-6 py-3">Evidence</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {alerts?.map((a, idx) => (
                                    <TableRow key={idx} onClick={() => onRowClick('alert', a)}>
                                        <Cell className="text-slate-500">{new Date(a.timestamp).toLocaleTimeString()}</Cell>
                                        <Cell><Badge variant="neutral">{a.rule_id}</Badge></Cell>
                                        <Cell><Badge variant={a.severity === 'HIGH' ? 'danger' : 'warning'}>{a.severity}</Badge></Cell>
                                        <Cell className="max-w-xs truncate text-xs font-mono text-slate-600" title={a.evidence}>{a.evidence}</Cell>
                                    </TableRow>
                                ))}
                            </tbody>
                        </table>
                    </Tabs.Content>
                </div>
            </Tabs.Root>
        </div>
    );
}
