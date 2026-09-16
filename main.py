"""
main.py — StudyPath AI FastAPI backend

Run with:
    uvicorn main:app --reload --port 8000

Docs at http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import knowledge_base
import graph_engine
import ai_engine
import quiz_engine
import recommendation_engine
import database
from models import QuizSubmission

app = FastAPI(
    title="StudyPath AI",
    description="Intelligent Personalized Learning System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "StudyPath AI backend is running", "docs": "/docs"}


# ---------------------------------------------------------------- Subjects
@app.get("/subjects")
def list_subjects():
    return knowledge_base.list_subjects()


# ------------------------------------------------------------------ Topics
@app.get("/topics")
def list_topics(subject_id: str = None):
    return knowledge_base.list_topics(subject_id)


@app.get("/topics/{topic_id}/content")
def get_topic_content(topic_id: str):
    result = ai_engine.explain_topic(topic_id)
    if not result:
        raise HTTPException(404, f"Topic '{topic_id}' not found")
    return result


@app.get("/topics/{topic_id}/path")
def get_learning_path(topic_id: str):
    """
    The 'What should I know first?' BFS/DFS traversal.
    Returns the ordered study path from foundational topic -> target topic.
    """
    path = graph_engine.get_learning_path(topic_id)
    if path is None:
        raise HTTPException(404, f"Topic '{topic_id}' not found")
    return {"topic_id": topic_id, "path": path}


@app.get("/topics/{topic_id}/next")
def get_next_topics(topic_id: str):
    if not knowledge_base.topic_exists(topic_id):
        raise HTTPException(404, f"Topic '{topic_id}' not found")
    return graph_engine.get_next_topics(topic_id)


# -------------------------------------------------------------------- Quiz
@app.get("/quiz/{topic_id}")
def get_quiz(topic_id: str):
    questions = knowledge_base.get_quiz(topic_id)
    if not questions:
        raise HTTPException(404, f"No quiz available for '{topic_id}'")
    # Strip correct answers before sending to client
    safe_questions = [{"q": q["q"], "options": q["options"]} for q in questions]
    return {"topic_id": topic_id, "questions": safe_questions}


@app.post("/quiz/{topic_id}/submit")
def submit_quiz(topic_id: str, submission: QuizSubmission):
    database.ensure_student(submission.student_id)
    result = quiz_engine.grade_quiz(topic_id, [a.dict() for a in submission.answers])
    if result is None:
        raise HTTPException(404, f"No quiz available for '{topic_id}'")

    database.save_quiz_attempt(
        student_id=submission.student_id,
        topic_id=topic_id,
        score=result["score"],
        total=result["total"],
        correct=result["correct"],
        weak_flag=result["weak"],
    )
    return result


# ------------------------------------------------------------- Student data
@app.get("/student/{student_id}/performance")
def student_performance(student_id: str):
    return recommendation_engine.analyze_performance(student_id)


@app.get("/student/{student_id}/recommend")
def student_recommendation(student_id: str):
    return recommendation_engine.recommend_next_topic(student_id)


@app.delete("/student/{student_id}/reset")
def reset_student(student_id: str):
    """Reset all quiz history for a student so new attempts are recorded fresh."""
    database.reset_student_data(student_id)
    return {"message": f"All quiz data for '{student_id}' has been reset."}
