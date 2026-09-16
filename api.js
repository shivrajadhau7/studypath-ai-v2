const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

export const api = {
  listTopics: () => request("/topics"),
  getPath: (topicId) => request(`/topics/${topicId}/path`),
  getContent: (topicId) => request(`/topics/${topicId}/content`),
  getQuiz: (topicId) => request(`/quiz/${topicId}`),
  submitQuiz: (topicId, studentId, answers) =>
    request(`/quiz/${topicId}/submit`, {
      method: "POST",
      body: JSON.stringify({ student_id: studentId, answers }),
    }),
  getPerformance: (studentId) => request(`/student/${studentId}/performance`),
  getRecommendation: (studentId) => request(`/student/${studentId}/recommend`),
  resetStudent: (studentId) =>
    request(`/student/${studentId}/reset`, { method: "DELETE" }),
};
