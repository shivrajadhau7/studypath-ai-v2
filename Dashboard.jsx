import React from "react";

export default function Dashboard({ performance, onReset }) {
  if (!performance) return null;
  const { total_attempts, average_score, weak_topics, history } = performance;

  const avgColor =
    average_score >= 70
      ? "var(--green)"
      : average_score >= 50
      ? "var(--amber)"
      : "var(--red)";

  return (
    <div className="card">
      <h2>
        <span className="step-num">4</span>
        Student Performance
      </h2>

      <div className="stat-row">
        <div className="stat">
          <div className="stat-value">{total_attempts}</div>
          <div className="stat-label">Attempts</div>
        </div>
        <div className="stat">
          <div className="stat-value" style={{ color: avgColor, WebkitTextFillColor: avgColor }}>
            {average_score}%
          </div>
          <div className="stat-label">Avg Score</div>
        </div>
        <div className="stat">
          <div
            className="stat-value"
            style={{
              color: weak_topics.length > 0 ? "var(--amber)" : "var(--green)",
              WebkitTextFillColor:
                weak_topics.length > 0 ? "var(--amber)" : "var(--green)",
            }}
          >
            {weak_topics.length}
          </div>
          <div className="stat-label">Weak Topics</div>
        </div>
      </div>

      {weak_topics.length > 0 && (
        <div className="weak-list">
          <div className="weak-list-title">⚠️ Topics needing review</div>
          <ul>
            {weak_topics.map((t) => (
              <li key={t.id}>{t.name}</li>
            ))}
          </ul>
        </div>
      )}

      {history.length > 0 && (
        <>
          <p
            style={{
              fontSize: "0.82rem",
              color: "var(--text-muted)",
              marginBottom: 8,
              textTransform: "uppercase",
              letterSpacing: "0.06em",
              fontWeight: 600,
            }}
          >
            Recent Attempts
          </p>
          <table className="history-table">
            <thead>
              <tr>
                <th>Topic</th>
                <th>Score</th>
                <th>Correct</th>
              </tr>
            </thead>
            <tbody>
              {history
                .slice()
                .reverse()
                .slice(0, 10)
                .map((h) => (
                  <tr key={h.id}>
                    <td>{h.topic_id.replace(/_/g, " ")}</td>
                    <td>
                      <span className={`score-pill ${h.score >= 60 ? "high" : "low"}`}>
                        {h.score}%
                      </span>
                    </td>
                    <td style={{ color: "var(--text-muted)" }}>
                      {h.correct}/{h.total}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </>
      )}

      <div className="dashboard-actions">
        <button
          id="reset-data-btn"
          className="danger-btn"
          onClick={onReset}
          title="Clear all quiz history and start fresh"
        >
          🗑 Reset All Data
        </button>
      </div>
    </div>
  );
}
