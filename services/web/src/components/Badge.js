import clsx from 'clsx';

export default function Badge({ children, variant = "neutral", className }) {
    const styles = {
        neutral: "bg-slate-100 text-slate-600 border-slate-200",
        success: "bg-green-50 text-green-700 border-green-200",
        warning: "bg-orange-50 text-orange-700 border-orange-200",
        danger: "bg-red-50 text-red-700 border-red-200",
        info: "bg-blue-50 text-blue-700 border-blue-200",
    };

    return (
        <span className={clsx(
            "px-2.5 py-0.5 rounded-full text-xs font-semibold border",
            styles[variant],
            className
        )}>
            {children}
        </span>
    );
}
