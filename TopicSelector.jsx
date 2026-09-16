import React from "react";

export default function TopicSelector({ topics, selectedTopic, onSelect }) {
  const icons = {
    process_management: "⚙️",
    processes: "🔄",
    cpu_scheduling: "🧮",
    fcfs: "📋",
    sjf: "⚡",
    round_robin: "🔁",
  };

  return (
    <div className="card">
      <h2>
        <span className="step-num">1</span>
        Choose a Topic
      </h2>
      <div className="topic-grid">
        {topics.map((t) => (
          <button
            key={t.id}
            id={`topic-btn-${t.id}`}
            className={`topic-btn ${selectedTopic === t.id ? "active" : ""}`}
            onClick={() => onSelect(t.id)}
          >
            <span>{icons[t.id] || "📚"}</span>
            {t.name}
          </button>
        ))}
      </div>
    </div>
  );
}
