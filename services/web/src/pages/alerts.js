import Layout from '../components/layout/Layout';
import Table from '../components/Table';
import Badge from '../components/Badge';
import useSWR from 'swr';
import { api, fetcher } from '../lib/api';

export default function Alerts() {
    const { data: alerts } = useSWR(api.getAlerts(), fetcher);

    return (
        <Layout>
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-slate-900">Anomalies & Alerts</h1>
                <p className="text-slate-500">Detected manipulations and rule violations.</p>
            </div>

            <Table
                headers={['Timestamp', 'Station ID', 'Rule', 'Severity', 'Evidence']}
                data={alerts}
                renderRow={(alert, i) => (
                    <tr key={i} className="hover:bg-slate-50">
                        <td className="px-6 py-4 text-sm text-slate-500">
                            {alert.timestamp || 'N/A'}
                        </td>
                        <td className="px-6 py-4 font-medium text-slate-700">{alert.stationId}</td>
                        <td className="px-6 py-4"><Badge variant="neutral">{alert.rule_id}</Badge></td>
                        <td className="px-6 py-4">
                            <Badge variant={alert.severity === 'HIGH' ? 'danger' : 'warning'}>
                                {alert.severity}
                            </Badge>
                        </td>
                        <td className="px-6 py-4 text-xs font-mono text-slate-600 max-w-md break-all">
                            {alert.evidence}
                        </td>
                    </tr>
                )}
            />
        </Layout>
    );
}
