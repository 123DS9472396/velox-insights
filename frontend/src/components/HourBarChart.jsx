import {
	Bar,
	BarChart,
	CartesianGrid,
	ResponsiveContainer,
	Tooltip,
	XAxis,
	YAxis,
} from "recharts";

export default function HourBarChart({ data, paymentBreakdown }) {
	return (
		<div className="panel">
			<h2>Trips by hour of day</h2>
			{data?.length ? (
				<div className="chart-wrap">
					<ResponsiveContainer width="100%" height="100%">
						<BarChart data={data}>
							<CartesianGrid stroke="rgba(148, 163, 184, 0.12)" vertical={false} />
							<XAxis dataKey="hour" tick={{ fill: "#9cb0d1" }} tickLine={false} axisLine={false} />
							<YAxis tick={{ fill: "#9cb0d1" }} tickLine={false} axisLine={false} />
							<Tooltip
								contentStyle={{
									background: "#08111f",
									border: "1px solid rgba(148, 163, 184, 0.2)",
									borderRadius: 12,
								}}
							/>
							<Bar dataKey="trips" fill="#7dd3fc" radius={[10, 10, 0, 0]} />
						</BarChart>
					</ResponsiveContainer>
				</div>
			) : (
				<div className="empty-state">No hourly data for the selected range.</div>
			)}

			<div style={{ height: 18 }} />
			<h2>Payment mix</h2>
			{paymentBreakdown?.length ? (
				<div className="grid" style={{ gap: 10 }}>
					{paymentBreakdown.map((row) => (
						<div key={row.payment_method} className="meta-card" style={{ padding: 16 }}>
							<div className="meta-label">{row.payment_method}</div>
							<div className="meta-value" style={{ fontSize: "1.2rem" }}>
								{row.trips.toLocaleString()} trips
							</div>
						</div>
					))}
				</div>
			) : (
				<div className="empty-state">No payment breakdown for the selected range.</div>
			)}
		</div>
	);
}
