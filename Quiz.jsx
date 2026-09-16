import React, { useState, useEffect } from "react";
import { api } from "../api";

export default function Quiz({ topicId, studentId, onGraded }) {
  const [questions, setQuestions] = useState([]);
  const [selections, setSelections] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    setResult(null);
    setSelections({});
    setLoading(true);
    api
      .getQuiz(topicId)
      .then((data) => setQuestions(data.questions))
      .catch(() => setQuestions([]))
      .finally(() => setLoading(false));
  }, [topicId]);

  const selectOption = (qIndex, optionIndex) => {
    setSelections((prev) => ({ ...prev, [qIndex]: optionIndex }));
  };

  const submit = async () => {
    setSubmitting(true);
    try {
      const answers = Object.entries(selections).map(
        ([question_index, selected_option]) => ({
          question_index: Number(question_index),
          selected_option,
        })
      );
      const res = await api.submitQuiz(topicId, studentId, answers);
      setResult(res);
      onGraded && onGraded(res);
    } finally {
      setSubmitting(false);
    }
  };

  const retakeQuiz = () => {
    setResult(null);
    setSelections({});
  };

  const answered = Object.keys(selections).length;
  const total = questions.length;
  const allAnswered = answered === total;

  if (loading)
    return (
      <div className="card loading-card">
        <span className="spinner" />
        Loading quiz…
      </div>
    );

  if (!questions.length)
    return (
      <div className="card">
        <h2>
          <span className="step-num">3</span>
          Quiz
        </h2>
        <p style={{ color: "var(--text-muted)", marginTop: 8 }}>
          No quiz available for this topic yet.
        </p>
      </div>
    );

  return (
    <div className="card">
      <div className="quiz-header">
        <h2 style={{ margin: 0 }}>
          <span className="step-num">3</span>
          Quiz
        </h2>
        <span className="quiz-progress">
          {answered}/{total} answered
        </span>
      </div>

      {questions.map((q, qi) => (
        <div className="quiz-question" key={qi}>
          <p className="q-text">
            {qi + 1}. {q.q}
          </p>
          <div className="q-options">
            {q.options.map((opt, oi) => (
              <label
                key={oi}
                id={`q${qi}-opt${oi}`}
                className={`q-option ${selections[qi] === oi ? "selected" : ""}`}
              >
                <input
                  type="radio"
                  name={`q-${qi}`}
                  checked={selections[qi] === oi}
                  onChange={() => selectOption(qi, oi)}
                />
                {opt}
              </label>
            ))}
          </div>
        </div>
      ))}

      <div className="quiz-actions">
        <button
          id="submit-quiz-btn"
          className="primary-btn"
          onClick={submit}
          disabled={!allAnswered || submitting}
        >
          {submitting ? (
            <>
              <span className="spinner" style={{ width: 14, height: 14, borderWidth: 2, verticalAlign: "middle", marginRight: 6 }} />
              Grading…
            </>
          ) : (
            "✅ Submit Quiz"
          )}
        </button>
        {result && (
          <button id="retake-quiz-btn" className="secondary-btn" onClick={retakeQuiz}>
            🔄 Retake
          </button>
        )}
      </div>

      {result && (
        <div className={`result-box ${result.weak ? "weak" : "strong"}`}>
          <div className="result-score">
            {result.weak ? "⚠️" : "🎉"} Score: {result.score}%{" "}
            <span style={{ fontSize: "0.85rem", fontWeight: 500, opacity: 0.75 }}>
              ({result.correct}/{result.total} correct)
            </span>
          </div>
          <p className="result-feedback">{result.feedback}</p>
        </div>
      )}
    </div>
  );
}
