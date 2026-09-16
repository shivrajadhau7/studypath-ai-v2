"""
ai_engine.py
-------------
The "AI Engine" box (NLP / ML / RAG) in the architecture diagram.

This ships with a deterministic, offline explanation generator so the
project runs with zero API keys and zero internet access. It is written
so you can drop in a real LLM call with a couple of lines.

To connect a real model (RAG over the knowledge base + an LLM for
generation), replace `explain_topic()` body with something like:

    from anthropic import Anthropic
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    context = knowledge_base.get_topic(topic_id)["content"]
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"Explain this to a student simply, using this "
                       f"verified context only:\n\n{context}\n\nTopic: {topic_id}"
        }]
    )
    return response.content[0].text

That's the whole RAG loop: the knowledge_base acts as your retrieval
source (swap it for a vector DB later if the content grows), and the LLM
call is the generation step.
"""

import knowledge_base


def explain_topic(topic_id: str) -> dict:
    topic = knowledge_base.get_topic(topic_id)
    if not topic:
        return None
    return {
        "id": topic_id,
        "name": topic["name"],
        "explanation": topic["content"],
        "estimated_minutes": topic["estimated_minutes"],
    }


def generate_weak_topic_feedback(topic_id: str, wrong_questions: list) -> str:
    """Simple rule-based feedback message (swap for an LLM call for richer output)."""
    topic = knowledge_base.get_topic(topic_id)
    name = topic["name"] if topic else topic_id
    if not wrong_questions:
        return f"Great job on {name}! No weak spots detected."
    return (
        f"You missed {len(wrong_questions)} question(s) on {name}. "
        f"Revisit: \"{topic['content'][:120]}...\" and retry the quiz."
    )
