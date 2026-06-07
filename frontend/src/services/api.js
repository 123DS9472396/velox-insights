import axios from "axios";

const api = axios.create({
	baseURL: import.meta.env.VITE_API_URL || "",
	timeout: 30000,
});

export async function fetchAnalytics(start, end) {
	const params = start && end ? { start, end } : undefined;
	const [kpis, daily, hourly, paymentBreakdown] = await Promise.all([
		api.get("/api/kpis"),
		api.get("/api/trips-by-day", { params }),
		api.get("/api/trips-by-hour", { params }),
		api.get("/api/payment-breakdown", { params }),
	]);

	return {
		kpis: kpis.data,
		daily: daily.data,
		hourly: hourly.data,
		paymentBreakdown: paymentBreakdown.data,
	};
}
