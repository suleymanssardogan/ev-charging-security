import { X } from 'lucide-react';
import * as Dialog from '@radix-ui/react-dialog';

export default function DetailDrawer({ open, onClose, data, type }) {
    if (!data) return null;

    return (
        <Dialog.Root open={open} onOpenChange={onClose}>
            <Dialog.Portal>
                <Dialog.Overlay className="fixed inset-0 bg-black/20 backdrop-blur-sm z-40 transition-opacity" />
                <Dialog.Content className="fixed top-0 right-0 h-full w-[450px] bg-white shadow-2xl z-50 p-0 border-l border-slate-200 outline-none transform transition-transform duration-300 ease-in-out">
                    {/* Header */}
                    <div className="bg-slate-50 px-6 py-4 border-b border-slate-200 flex items-center justify-between">
                        <div>
                            <Dialog.Title className="text-lg font-bold text-slate-900 capitalize">
                                {type} Details
                            </Dialog.Title>
                            <Dialog.Description className="text-xs text-slate-500 font-mono mt-1">
                                ID: {data.transactionId || data.rule_id || 'N/A'}
                            </Dialog.Description>
                        </div>
                        <button onClick={() => onClose(false)} className="text-slate-400 hover:text-slate-600 p-1 hover:bg-slate-200 rounded-full transition-colors">
                            <X size={20} />
                        </button>
                    </div>

                    {/* Body */}
                    <div className="p-6 overflow-y-auto h-[calc(100%-80px)]">
                        <div className="space-y-6">

                            {/* Context Info */}
                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                    <div className="text-xs text-slate-400 uppercase font-semibold">Station ID</div>
                                    <div className="font-medium text-slate-700">{data.stationId || data.chargePointId || '-'}</div>
                                </div>
                                <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                                    <div className="text-xs text-slate-400 uppercase font-semibold">Time</div>
                                    <div className="font-medium text-slate-700">{data.timestamp ? new Date(data.timestamp).toLocaleString() : '-'}</div>
                                </div>
                            </div>

                            {/* Evidence / JSON Dump */}
                            <div>
                                <h4 className="text-sm font-bold text-slate-800 mb-2">Metadata & Evidence</h4>
                                <pre className="bg-slate-900 text-slate-50 p-4 rounded-lg text-xs font-mono overflow-auto max-h-96">
                                    {JSON.stringify(data, null, 2)}
                                </pre>
                            </div>

                        </div>
                    </div>
                </Dialog.Content>
            </Dialog.Portal>
        </Dialog.Root>
    );
}
