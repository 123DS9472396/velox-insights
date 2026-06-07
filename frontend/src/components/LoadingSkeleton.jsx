export default function LoadingSkeleton() {
	return (
		<>
			<div className="loading-grid">
				{Array.from({ length: 4 }).map((_, index) => (
					<div className="kpi-card skeleton" key={index} />
				))}
			</div>

			<div className="content-grid" style={{ marginTop: 18 }}>
				<div className="panel skeleton" style={{ minHeight: 420 }} />
				<div className="panel skeleton" style={{ minHeight: 420 }} />
			</div>
		</>
	);
}
