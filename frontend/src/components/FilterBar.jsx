export default function FilterBar({ filters, setFilters, onRefresh }) {
	return (
		<section className="filter-bar">
			<div className="field">
				<label htmlFor="startDate">Start date</label>
				<input
					id="startDate"
					type="date"
					value={filters.startDate}
					onChange={(event) => setFilters((current) => ({ ...current, startDate: event.target.value }))}
				/>
			</div>

			<div className="field">
				<label htmlFor="endDate">End date</label>
				<input
					id="endDate"
					type="date"
					value={filters.endDate}
					onChange={(event) => setFilters((current) => ({ ...current, endDate: event.target.value }))}
				/>
			</div>

			<div className="action-row">
				<button className="button" type="button" onClick={onRefresh}>
					Refresh analytics
				</button>
			</div>

			<div className="action-row">
				<button
					className="button secondary"
					type="button"
					onClick={() => setFilters({ startDate: "2023-01-01", endDate: "2023-01-31" })}
				>
					Reset range
				</button>
			</div>
		</section>
	);
}
