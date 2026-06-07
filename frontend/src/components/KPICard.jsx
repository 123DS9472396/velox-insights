export default function KPICard({ label, value, unit = "" }) {
	const displayValue =
		typeof value === "number"
			? Number.isInteger(value)
				? value.toLocaleString()
				: value.toLocaleString(undefined, { maximumFractionDigits: 2 })
			: value ?? "—";

	return (
		<article className="kpi-card">
			<div className="kpi-label">{label}</div>
			<div className="kpi-value">
				{displayValue}
				{unit ? <span className="kpi-unit">{unit}</span> : null}
			</div>
		</article>
	);
}
