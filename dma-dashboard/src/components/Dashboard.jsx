import { useState } from "react";
import { runBacktest } from "../service/backtestService";
import BacktestForm from "./BacktestForm";
import SMACharts from "./SMACharts";
import SummaryCard from "./SummaryCard";

export default function Dashboard() {
    const [activeTab, setActiveTab] = useState("portfolio");
    const [backtestData, setBacktestData] = useState(null);
    const [loading, setLoading] = useState(false);
    
    const handleRunBacktest = async ({ ticker, startDate, endDate, amount }) => {
        try {
            setLoading(true);
            const result = await runBacktest(ticker, startDate, endDate, amount);
            setBacktestData(result);
        } catch (err) {
            console.error(err);
            alert("Something went wrong");
        } finally {
            setLoading(false);
        }
    };

    const transformedData = backtestData?.results?.map((entry) => ({
        date: entry.date,
        portfolio_value: entry.portfolio_value,
      })) || [];

      const yearlyReturn = backtestData?.yearly_return;
      const formattedYearlyReturn = yearlyReturn ? Object.entries(yearlyReturn).map(([year,value]) => ({
        Year: parseInt(year),
        yearly_return: value,
      })) : [];

      const summary = backtestData?.summary;

    return (
        <div className="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-6">
            <div className="max-w-5xl mx-auto space-y-8">
                <div className="bg-white dark:bg-gray-800 p-6 rounded shadow">
                    <BacktestForm onSubmit={handleRunBacktest}/>
                    {loading && <p className="mt-2 text-sm text-gray-500">Running backtest...</p>}
                </div>
            </div>
            <br></br>
            <div className="max-w-5xl mx-auto space-y-8 border-gray-100">
                <button onClick={() => setActiveTab("portfolio")} className={`pb-2 px-4 font-medium ${
                    activeTab === "portfolio" ? "border-b-2 border-indigo-600 text-indigo-600" : "text-gray-500"
                }`}>
                    Portfolio Value
                </button>
                <button onClick={() => setActiveTab("yearly")} className={`pb-2 px-4 font-medium ${
                    activeTab === "yearly" ? "border-b-2 border-indigo-600 text-indigo-600" : "text-gray-500"
                }`}>
                    Yearly Return
                </button>
            </div>
            <div className="max-w-5xl mx-auto space-y-8">
                <div className="bg-white dark:bg-gray-800 p-6 rounded shadow">
                    {transformedData.length > 0 && <SMACharts data={transformedData} yearlyReturn={formattedYearlyReturn} activeTab={activeTab} />}
                </div>
            </div>
            <div className="max-w-5xl mx-auto space-y-8">
                <div className="bg-white dark:bg-gray-800 p-6 rounded shadow">
                    <SummaryCard summary={summary}/>
                </div>
            </div>
        </div>
    );
}
