"""
quiz_engine.py
---------------
Scores a quiz submission and determines weak-topic flags.
"""

import knowledge_base
import ai_engine


def grade_quiz(topic_id: str, answers: list):
    """
    answers: list of {"question_index": int, "selected_option": int}
    """
    questions = knowledge_base.get_quiz(topic_id)
    if not questions:
        return None

    answer_map = {a["question_index"]: a["selected_option"] for a in answers}
    correct = 0
    wrong_indices = []

    for i, q in enumerate(questions):
        selected = answer_map.get(i)
        if selected is not None and selected == q["answer"]:
            correct += 1
        else:
            wrong_indices.append(i)

    total = len(questions)
    score = round((correct / total) * 100, 1) if total else 0.0
    weak = score < 60

    wrong_questions = [questions[i] for i in wrong_indices]
    feedback = ai_engine.generate_weak_topic_feedback(topic_id, wrong_questions)

    return {
        "topic_id": topic_id,
        "total": total,
        "correct": correct,
        "score": score,
        "weak": weak,
        "feedback": feedback,
        "wrong_question_indices": wrong_indices,
    }
