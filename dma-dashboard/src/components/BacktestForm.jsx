import { useState } from "react";

export default function BacktestForm({ onSubmit }) {
    const [amount,setAmount] = useState(0);
    const [ticker, setTicker] = useState("");
    const [startDate, setStartDate] = useState("2020-01-01");
    const [endDate, setEndDate] = useState("2024-12-31");
    const [errors, setErrors] = useState({ ticker: "", amount: "" });

    const handleSubmit = (e) => {
        e.preventDefault();
        const newErrors = { ticker: "", amount: "" };
        let hasError = false;
        if (!ticker.trim()) {
            newErrors.ticker = "Ticker cannot be empty.";
            hasError = true;
        }

        if (!amount || isNaN(amount) || Number(amount) <= 0) {
            newErrors.amount = "Amount must be a positive number.";
            hasError = true;
        }

        if (hasError) {
            setErrors(newErrors);
            return;
        }

        setErrors({ ticker: "", amount: "" }); // clear on success


        onSubmit({
            ticker: ticker.toUpperCase(),
            startDate,
            endDate,
            amount
        });
        setTicker("");
        setAmount(0);
    };

    const inputStyles =
        "w-full border border-gray-300 px-3 py-2 rounded shadow-sm " +
        "bg-white text-black placeholder-gray-500 " +
        "dark:bg-gray-800 dark:text-white dark:placeholder-gray-400 dark:border-gray-600 " +
        "transition-colors duration-200";

    return (
        <form onSubmit={handleSubmit} className="space-y-6 max-w-d">
            <div>
                <label className="block text-sm font-medium mb-1">Ticker</label>
                <input type="text" placeholder="(e.g. AAPL)" value={ticker} onChange={(e) => setTicker(e.target.value)} className= {inputStyles}/>
                {errors.ticker && (<p className="text-red-500 text-sm mt-1">{errors.ticker}</p>)}
            </div>
            <div className="flex gap-4">
                <div className="flex-1">
                    <label className="block text-sm font-medium mb-1">Start Date</label>
                    <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} className={inputStyles}></input>
                </div>
                <div className="flex-1">
                    <label className="block text-sm font-medium mb-1">End Date</label>
                    <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} className={inputStyles}></input>
                </div>
            </div>
            <div>
                <label className="block text-sm font-medium mb-1">Amount</label>
                <input type="text" placeholder="(e.g. 100000)" value={amount} onChange={(e) => setAmount(e.target.value)} className={inputStyles}/>
                {errors.amount && (<p className="text-red-500 text-sm mt-1">{errors.amount}</p>)}
            </div>

            <button type="submit" className="ring bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 w-full">Run backtest</button>
        </form>
    );
}