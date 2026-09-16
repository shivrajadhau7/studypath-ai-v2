import React from "react";

const ACTION_META = {
  review:   { label: "Review Recommended",  cls: "badge-review"   },
  advance:  { label: "Next Topic Ready 🚀",  cls: "badge-advance"  },
  start:    { label: "Get Started",          cls: "badge-start"    },
  complete: { label: "Path Complete 🎉",     cls: "badge-complete" },
};

export default function Recommendations({ recommendation, onJump }) {
  if (!recommendation) return null;
  const meta = ACTION_META[recommendation.action] || { label: "Recommendation", cls: "badge-advance" };

  return (
    <div className="card recommend-card">
      <h2>
        <span className="step-num">5</span>
        Next Recommended Topic
      </h2>
      <div className="recommend-box">
        <span id="recommendation-badge" className={`badge ${meta.cls}`}>
          {meta.label}
        </span>
        {recommendation.topic_name && (
          <h3>{recommendation.topic_name}</h3>
        )}
        <p>{recommendation.reason}</p>
        {recommendation.topic_id && (
          <button
            id="goto-recommendation-btn"
            className="primary-btn"
            onClick={() => onJump(recommendation.topic_id)}
          >
            Go to {recommendation.topic_name} →
          </button>
        )}
      </div>
    </div>
  );
}
