"""
knowledge_base.py
------------------
Loads the topic/subject data (the "Knowledge Base" box in the architecture
diagram) and exposes simple lookup helpers used by the AI / Algorithm engines.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

with open(os.path.join(DATA_DIR, "topics.json"), encoding="utf-8") as f:
    _RAW = json.load(f)

with open(os.path.join(DATA_DIR, "quiz_bank.json"), encoding="utf-8") as f:
    QUIZ_BANK = json.load(f)

# Flatten all topics across all subjects into one dict keyed by topic id
TOPICS = {}
SUBJECTS = {}
for subject_id, subject in _RAW.items():
    SUBJECTS[subject_id] = subject["subject_name"]
    for topic_id, topic in subject["topics"].items():
        topic["subject_id"] = subject_id
        TOPICS[topic_id] = topic


def list_subjects():
    return [{"id": sid, "name": name} for sid, name in SUBJECTS.items()]


def list_topics(subject_id=None):
    topics = TOPICS.values()
    if subject_id:
        topics = [t for t in topics if t["subject_id"] == subject_id]
    return [{"id": t["id"], "name": t["name"], "subject_id": t["subject_id"]} for t in topics]


def get_topic(topic_id):
    return TOPICS.get(topic_id)


def get_quiz(topic_id):
    return QUIZ_BANK.get(topic_id, [])


def topic_exists(topic_id):
    return topic_id in TOPICS
