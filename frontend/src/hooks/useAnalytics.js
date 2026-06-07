import { useCallback, useEffect, useState } from "react";
import { fetchAnalytics } from "../services/api";

const DEFAULT_RANGE = {
	startDate: "2015-01-01",
	endDate: "2015-01-31",
};

export function useAnalytics(initialRange = DEFAULT_RANGE) {
	const [filters, setFilters] = useState(initialRange);
	const [kpis, setKpis] = useState(null);
	const [daily, setDaily] = useState([]);
	const [hourly, setHourly] = useState([]);
	const [paymentBreakdown, setPaymentBreakdown] = useState([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(null);

	const load = useCallback(async () => {
		setLoading(true);
		setError(null);

		try {
			const payload = await fetchAnalytics(filters.startDate, filters.endDate);
			setKpis(payload.kpis);
			setDaily(payload.daily);
			setHourly(payload.hourly);
			setPaymentBreakdown(payload.paymentBreakdown || []);
		} catch (err) {
			setError(err instanceof Error ? err.message : "Failed to load analytics");
		} finally {
			setLoading(false);
		}
	}, [filters.endDate, filters.startDate]);

	useEffect(() => {
		load();
	}, [load]);

	return {
		kpis,
		daily,
		hourly,
		paymentBreakdown,
		filters,
		setFilters,
		loading,
		error,
		refresh: load,
	};
}
