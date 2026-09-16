"""
recommendation_engine.py
--------------------------
Decides "Next Recommended Topic" using quiz performance history.

Logic:
  1. Look at the student's weak topics (score < 60% on latest attempt).
  2. If there are weak prerequisite topics, recommend re-studying the
     weakest one first (you shouldn't move on with a shaky foundation).
  3. Otherwise, walk the DAG forward from the most recently passed topic
     and recommend the next unattempted child topic.
"""

import database
import graph_engine
import knowledge_base


def recommend_next_topic(student_id: str):
    attempts = database.get_attempts(student_id)
    weak_topics = database.get_weak_topics(student_id)

    if weak_topics:
        # Recommend the lowest-scoring weak topic for review
        latest_scores = {}
        for a in attempts:
            latest_scores[a["topic_id"]] = a["score"]
        weakest = min(weak_topics, key=lambda t: latest_scores.get(t, 0))
        topic = knowledge_base.get_topic(weakest)
        return {
            "action": "review",
            "topic_id": weakest,
            "topic_name": topic["name"] if topic else weakest,
            "reason": f"Your last score on this topic was {latest_scores.get(weakest, 0):.0f}%. "
                      f"Strengthen this before moving forward.",
        }

    if not attempts:
        return {
            "action": "start",
            "topic_id": "process_management",
            "topic_name": "Process Management",
            "reason": "No quiz attempts yet — start from the foundational topic.",
        }

    # Find topics with the highest score among most-recently attempted, then look at its children
    last_attempt = attempts[-1]
    children = graph_engine.get_next_topics(last_attempt["topic_id"])
    attempted_ids = {a["topic_id"] for a in attempts}
    next_candidates = [c for c in children if c["id"] not in attempted_ids]

    if next_candidates:
        nxt = next_candidates[0]
        return {
            "action": "advance",
            "topic_id": nxt["id"],
            "topic_name": nxt["name"],
            "reason": f"You've mastered {knowledge_base.get_topic(last_attempt['topic_id'])['name']} — "
                      f"time to move on.",
        }

    return {
        "action": "complete",
        "topic_id": None,
        "topic_name": None,
        "reason": "You've covered every topic in this path with a passing score. Great work!",
    }


def analyze_performance(student_id: str):
    attempts = database.get_attempts(student_id)
    weak = database.get_weak_topics(student_id)
    total_attempts = len(attempts)
    avg_score = sum(a["score"] for a in attempts) / total_attempts if total_attempts else 0
    return {
        "total_attempts": total_attempts,
        "average_score": round(avg_score, 1),
        "weak_topics": [
            {"id": t, "name": knowledge_base.get_topic(t)["name"] if knowledge_base.get_topic(t) else t}
            for t in weak
        ],
        "history": attempts,
    }
