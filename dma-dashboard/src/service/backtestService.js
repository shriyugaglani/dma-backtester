// Get API URL from environment variable or default to localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const runBacktest = async(ticker, startDate, endDate, amount) => {
    const response = await fetch(`${API_BASE_URL}/api/v1/run-backtest`, {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ ticker,startDate,endDate, amount }),
    });

    if (!response.ok) {
        throw new Error("Backtest Failed"); // ✅ correct
    }

    return await response.json();
}