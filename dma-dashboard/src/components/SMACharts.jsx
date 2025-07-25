import {
  LineChart,
  BarChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Cell,
} from "recharts";

export default function SMACharts({ data, yearlyReturn, activeTab }) {
  console.log("Yearly Return:", yearlyReturn);
  return (
    <div style={{ width: "100%", height: "500px", border: "1px solid #ccc" }}>
      {activeTab === "portfolio" && (
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip formatter={(val) => `$${Number(val).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`} />
            <Line
              type="monotone"
              dataKey="portfolio_value"
              stroke="#8884d8"
              name="Portfolio Value"
            />
          </LineChart>
        </ResponsiveContainer>
      )}
      {activeTab === "yearly" && (
        <ResponsiveContainer width="100%" height="100%">
            <BarChart data={yearlyReturn}>
                <CartesianGrid strokeDasharray="3 3"/>
                <XAxis dataKey="Year"/>
                <YAxis tickFormatter={(v) => `${(v * 100).toFixed(1)}%`} />
                <Tooltip 
                formatter={(val) => `${(val * 100).toFixed(2)}%`}
                />
                <Bar dataKey="yearly_return"
                name="Yearly Return">
                {yearlyReturn.map((entry, index) => (
                    <Cell
                    key={`cell-${index}`}
                    fill={entry.yearly_return >= 0 ? "#34d399" : "#f87171"}
                    />
                ))}
                </Bar>
            </BarChart>
        </ResponsiveContainer>
      )}
      
    </div>
  );
}
