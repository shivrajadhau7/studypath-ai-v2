"""
models.py — Pydantic request/response schemas.
"""

from pydantic import BaseModel
from typing import List, Optional


class QuizAnswer(BaseModel):
    question_index: int
    selected_option: int


class QuizSubmission(BaseModel):
    student_id: str
    answers: List[QuizAnswer]


class QuizResult(BaseModel):
    topic_id: str
    total: int
    correct: int
    score: float
    weak: bool
    feedback: str
    wrong_question_indices: List[int]
