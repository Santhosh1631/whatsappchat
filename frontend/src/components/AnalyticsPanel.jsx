function AnalyticsPanel({ analytics, summary, sentiment, onExport }) {
  return (
    <section className="analytics-panel">
      <div className="card">
        <h3>Total Messages</h3>
        <p>{analytics?.total_messages ?? 0}</p>
      </div>
      <div className="card">
        <h3>Most Active User</h3>
        <p>
          {analytics?.most_active_user
            ? `${analytics.most_active_user.name} (${analytics.most_active_user.count})`
            : 'No data'}
        </p>
      </div>
      <div className="card">
        <h3>Sentiment</h3>
        <p>{sentiment?.label || 'neutral'}</p>
      </div>
      <div className="card wide">
        <h3>AI Summary</h3>
        <p>{summary || 'No summary yet.'}</p>
      </div>
      <div className="card wide">
        <h3>Messages Per Day</h3>
        <div className="pill-row">
          {(analytics?.messages_per_day || []).slice(-10).map((d) => (
            <span key={d.date} className="pill">
              {d.date}: {d.count}
            </span>
          ))}
        </div>
      </div>
      <div className="card wide">
        <h3>Top Words</h3>
        <div className="pill-row">
          {(analytics?.word_frequency || []).slice(0, 15).map((w) => (
            <span key={w.word} className="pill">
              {w.word} ({w.count})
            </span>
          ))}
        </div>
      </div>
      <button className="export-btn" onClick={onExport}>Export Parsed JSON</button>
    </section>
  );
}

export default AnalyticsPanel;
