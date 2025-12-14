import Layout from '../components/layout/Layout';

export default function Settings() {
    return (
        <Layout>
            <div className="mb-8">
                <h1 className="text-2xl font-bold text-slate-900">Settings</h1>
                <p className="text-slate-500">System configuration and API endpoints.</p>
            </div>
            <div className="bg-white p-8 rounded-xl border border-slate-200 text-center text-slate-500">
                Configuration is managed via Docker environment variables in this demo.
            </div>
        </Layout>
    );
}
