export default function SummaryCard({ summary }) {
    if (!summary) return null;

    const stats = [
        { label: "Total Return", value: summary.total_return },
        { label: "Annualized Return ", value: summary.annualized_return },
        { label: "Sharpe Ratio", value: summary.sharpe_ratio },
        { label: "Max Drawdown", value: summary.max_drawdown },
        { label: "Win Rate", value: summary.win_rate },
        { label: "Trades", value: summary.num_trades },
        { label: "Years", value: summary.years },
    ]

    return (
        <div className="grid grid-cols sm:grid-cols-3 gap-4 my-6">
            {stats.map((item,idx) => (
                <div key={idx} className="border-separate rounded-2xl border-spacing-2 border border-gray-400 dark:border-gray-500">
                    <div className="text-sm text-gray-500 text-center dark:text-gray-400 mb-1 uppercase tracking-wide">{item.label}</div>
                    <div className=":text-2xl font-bold text-center text-indigo-600 dark:text-indigo-400">{item.value}</div>
                </div>
            ))}
        </div>
    );
}