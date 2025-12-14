import Layout from '../components/layout/Layout';
import Table from '../components/Table';
import Badge from '../components/Badge';
import useSWR from 'swr';
import { api, fetcher } from '../lib/api';

export default function Invoices() {
    const { data: invoices } = useSWR(api.getInvoices(), fetcher);

    return (
        <Layout>
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-slate-900">Invoices</h1>
                <p className="text-slate-500">Billing history and generated invoices.</p>
            </div>

            <Table
                headers={['Transaction ID', 'Charge Point', 'Total kWh', 'Total Cost', 'Status', 'Review']}
                data={invoices}
                renderRow={(inv, i) => (
                    <tr key={i} className="hover:bg-slate-50">
                        <td className="px-6 py-4 font-medium text-slate-700">{inv.transactionId}</td>
                        <td className="px-6 py-4 text-slate-500">{inv.chargePointId}</td>
                        <td className="px-6 py-4 text-slate-600">{inv.totalKwh} kWh</td>
                        <td className="px-6 py-4 font-bold text-slate-700">${inv.totalCost?.toFixed(2)}</td>
                        <td className="px-6 py-4"><Badge variant="success">{inv.status}</Badge></td>
                        <td className="px-6 py-4">
                            {/* Placeholder for manual review logic */}
                            <span className="text-xs text-slate-400">Auto-Approved</span>
                        </td>
                    </tr>
                )}
            />
        </Layout>
    );
}
