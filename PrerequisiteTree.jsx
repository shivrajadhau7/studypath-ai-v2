import React from "react";

export default function PrerequisiteTree({ path, content, onSelectExplain }) {
  if (!path) return null;
  return (
    <div className="card">
      <h2>
        <span className="step-num">2</span>
        What should I know first?
      </h2>
      <p className="hint">
        Study order (foundational → target) found via BFS/DFS over the prerequisite graph.
        Click any node to view its explanation.
      </p>
      <div className="path-chain">
        {path.map((step, i) => (
          <React.Fragment key={step.id}>
            <div
              id={`path-node-${step.id}`}
              className={`path-node ${step.is_target ? "target" : ""}`}
              onClick={() => onSelectExplain(step.id)}
              title="Click to view explanation"
            >
              <div className="path-node-name">{step.name}</div>
              <div className="path-node-time">⏱ {step.estimated_minutes} min</div>
            </div>
            {i < path.length - 1 && <div className="path-arrow">↓</div>}
          </React.Fragment>
        ))}
      </div>

      {content && (
        <div className="explanation-box">
          <h3>📖 {content.name}</h3>
          <p>{content.explanation}</p>
        </div>
      )}
    </div>
  );
}
