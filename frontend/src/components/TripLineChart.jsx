import {
	CartesianGrid,
	Line,
	LineChart,
	ResponsiveContainer,
	Tooltip,
	XAxis,
	YAxis,
} from "recharts";

export default function TripLineChart({ data }) {
	return (
		<div className="panel">
			<h2>Daily trips and revenue</h2>
			{data?.length ? (
				<div className="chart-wrap" style={{minHeight: 260}}>
					<ResponsiveContainer width="100%" height="100%">
						<LineChart data={data}>
							<CartesianGrid stroke="rgba(148, 163, 184, 0.12)" vertical={false} />
							<XAxis dataKey="date" tick={{ fill: "#9cb0d1" }} tickLine={false} axisLine={false} />
							<YAxis tick={{ fill: "#9cb0d1" }} tickLine={false} axisLine={false} />
							<Tooltip
								contentStyle={{
									background: "#08111f",
									border: "1px solid rgba(148, 163, 184, 0.2)",
									borderRadius: 12,
								}}
							/>
							<Line type="monotone" dataKey="trips" stroke="#7dd3fc" strokeWidth={3} dot={false} />
							<Line type="monotone" dataKey="revenue" stroke="#f59e0b" strokeWidth={3} dot={false} />
						</LineChart>
					</ResponsiveContainer>
				</div>
			) : (
				<div className="empty-state">No day-level data for the selected range.</div>
			)}
		</div>
	);
}
