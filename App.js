import React, { useState, useEffect, useCallback } from "react";
import { api } from "./api";
import TopicSelector from "./components/TopicSelector";
import PrerequisiteTree from "./components/PrerequisiteTree";
import Quiz from "./components/Quiz";
import Dashboard from "./components/Dashboard";
import Recommendations from "./components/Recommendations";

const STUDENT_ID = "demo_student"; // swap for real auth/session later

export default function App() {
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState(null);
  const [path, setPath] = useState(null);
  const [content, setContent] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.listTopics().then(setTopics).catch((e) => setError(e.message));
  }, []);

  const loadStudentData = useCallback(() => {
    api.getPerformance(STUDENT_ID).then(setPerformance).catch(() => {});
    api.getRecommendation(STUDENT_ID).then(setRecommendation).catch(() => {});
  }, []);

  useEffect(() => {
    loadStudentData();
  }, [loadStudentData]);

  const handleSelectTopic = async (topicId) => {
    setSelectedTopic(topicId);
    setContent(null);
    setError(null);
    try {
      const pathData = await api.getPath(topicId);
      setPath(pathData.path);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleExplain = async (topicId) => {
    try {
      const c = await api.getContent(topicId);
      setContent(c);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleQuizGraded = () => {
    loadStudentData();
  };

  const handleReset = async () => {
    if (!window.confirm("Reset all quiz data for this session? This cannot be undone.")) return;
    try {
      await api.resetStudent(STUDENT_ID);
      setPerformance(null);
      setRecommendation(null);
      loadStudentData();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-badge">✨ AI-Powered Learning</div>
        <h1>🧠 StudyPath AI</h1>
        <p>Intelligent Personalized Learning System</p>
      </header>

      {error && (
        <div className="error-banner">
          ⚠️ {error} — is the backend running on :8000?
        </div>
      )}

      <main className="app-main">
        <TopicSelector
          topics={topics}
          selectedTopic={selectedTopic}
          onSelect={handleSelectTopic}
        />

        {selectedTopic && (
          <PrerequisiteTree
            path={path}
            content={content}
            onSelectExplain={handleExplain}
          />
        )}

        {selectedTopic && (
          <Quiz
            topicId={selectedTopic}
            studentId={STUDENT_ID}
            onGraded={handleQuizGraded}
          />
        )}

        <Dashboard performance={performance} onReset={handleReset} />

        <Recommendations recommendation={recommendation} onJump={handleSelectTopic} />
      </main>
    </div>
  );
}
