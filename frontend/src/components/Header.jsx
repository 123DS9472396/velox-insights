export default function Header() {
	return (
		<section className="hero">
			<div className="hero-card">
				<span className="eyebrow">Velox Insights</span>
				<h1>NYC Taxi Analytics</h1>
				<p>
					ClickHouse-powered taxi analytics with a dbt medallion pipeline and a React dashboard for
					fast KPI exploration.
				</p>
			</div>

			<div className="hero-meta">
				<div className="meta-card">
					<div className="meta-label">Architecture</div>
					<div className="meta-value">ClickHouse + dbt + FastAPI + React</div>
				</div>
				<div className="meta-card">
					<div className="meta-label">Pipeline</div>
					<div className="meta-value">Bronze → Silver → Gold</div>
				</div>
			</div>
		</section>
	);
}
