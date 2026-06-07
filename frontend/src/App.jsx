import Header from "./components/Header";
import KPICard from "./components/KPICard";
import FilterBar from "./components/FilterBar";
import LoadingSkeleton from "./components/LoadingSkeleton";
import TripLineChart from "./components/TripLineChart";
import HourBarChart from "./components/HourBarChart";
import { useAnalytics } from "./hooks/useAnalytics";

export default function App() {
	const { kpis, daily, hourly, paymentBreakdown, filters, setFilters, loading, error, refresh } =
		useAnalytics();

	return (
		<main className="app-shell">
			<Header />

			<FilterBar filters={filters} setFilters={setFilters} onRefresh={refresh} />

			{loading ? (
				<LoadingSkeleton />
			) : error ? (
				<div className="error-state">{error}</div>
			) : (
				<>
					<section className="kpi-grid">
						<KPICard label="Total trips" value={kpis?.total_trips ?? 0} />
						<KPICard label="Revenue" value={kpis?.total_revenue ?? 0} unit="$" />
						<KPICard label="Avg distance" value={kpis?.avg_distance ?? 0} unit="mi" />
						<KPICard label="Avg duration" value={kpis?.avg_duration_min ?? 0} unit="min" />
					</section>

					<section className="content-grid">
						<TripLineChart data={daily} />
						<HourBarChart data={hourly} paymentBreakdown={paymentBreakdown} />
					</section>
				</>
			)}
		</main>
	);
}
