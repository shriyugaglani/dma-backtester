export const runBacktest = async(ticker, startDate, endDate, amount) => {
    const response = await fetch("http://localhost:8000/run-backtest", {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ ticker,startDate,endDate, amount }),
    });

    if (!response.ok) {
        throw new Error("Backtest Failed"); // ✅ correct
    }

    return await response.json();
}