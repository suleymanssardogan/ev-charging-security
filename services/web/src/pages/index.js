import { useState } from 'react';
import useSWR, { useSWRConfig } from 'swr';
import { api, fetcher } from '../lib/api';

// Components
import Layout from '../components/layout/Layout';
import ScenarioRunnerBar from '../components/widgets/ScenarioRunnerBar';
import KpiStrip from '../components/widgets/KpiStrip';
import MasterGrid from '../components/widgets/MasterGrid';
import { KwhTimeSeries, AlertTimeline } from '../components/charts/ChartComponents';
import DetailDrawer from '../components/widgets/DetailDrawer';

export default function DashboardPage() {
    const { mutate } = useSWRConfig();
    const { data: sessions } = useSWR(api.getInvoices(), fetcher, { refreshInterval: 2000 }); // Using invoices as sessions proxy for now
    const { data: alerts } = useSWR(api.getAlerts(), fetcher, { refreshInterval: 2000 });

    // Drawer State
    const [drawerOpen, setDrawerOpen] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const [selectedType, setSelectedType] = useState(null);

    const handleRowClick = (type, item) => {
        setSelectedType(type);
        setSelectedItem(item);
        setDrawerOpen(true);
    };

    const handleRunComplete = () => {
        // Invalidate/Refetch data
        mutate(api.getInvoices());
        mutate(api.getAlerts());
    };

    // KPI Calculations
    const totalCost = sessions ? sessions.reduce((acc, s) => acc + (s.totalCost || 0), 0).toFixed(2) : '0.00';
    const totalKwh = sessions ? sessions.reduce((acc, s) => acc + (s.totalKwh || 0), 0).toFixed(1) : '0.0';
    const activeAlerts = alerts ? alerts.length : 0;

    // Chart Data Preparation
    const chartData = sessions ? sessions.map((s, i) => ({
        time: i,
        value: s.totalKwh
    })).slice(-20) : [];

    const alertChartData = alerts ? alerts.reduce((acc, curr) => {
        // Simple grouping by rule (mocking time series for now)
        const existing = acc.find(a => a.time === curr.rule_id);
        if (existing) existing.count++;
        else acc.push({ time: curr.rule_id, count: 1 });
        return acc;
    }, []) : [];

    return (
        <div className="min-h-screen bg-slate-100 text-slate-900 font-sans">
            {/* Sidebar Layout */}
            <Layout>
                <div className="flex flex-col gap-6">

                    {/* 1. Control Bar */}
                    <ScenarioRunnerBar onRunComplete={handleRunComplete} />

                    {/* 2. KPI Strip */}
                    <KpiStrip
                        totalCost={totalCost}
                        totalKwh={totalKwh}
                        activeAlerts={activeAlerts}
                        sessionCount={sessions ? sessions.length : 0}
                    />

                    {/* 3. Charts Grid */}
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <KwhTimeSeries data={chartData} />
                        <AlertTimeline data={alertChartData} />
                    </div>

                    {/* 4. Master Data Grid */}
                    <MasterGrid
                        sessions={sessions} // Using invoices/sessions interchangeably for MVP structure
                        invoices={sessions}
                        alerts={alerts}
                        onRowClick={handleRowClick}
                    />

                </div>
            </Layout>

            {/* 5. Detail Drawer */}
            <DetailDrawer
                open={drawerOpen}
                onClose={setDrawerOpen}
                data={selectedItem}
                type={selectedType}
            />
        </div>
    );
}
