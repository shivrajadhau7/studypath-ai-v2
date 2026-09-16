# 🧠 StudyPath AI — Intelligent Personalized Learning System

A working prototype of the system in your architecture diagram: a student picks a
topic (e.g. **CPU Scheduling**), the system figures out *what they need to know
first* using graph traversal (BFS/DFS over a prerequisite DAG), teaches the chain
of topics, quizzes the student, tracks performance, detects weak topics, and
recommends what to study next.

```
CPU Scheduling → What should I know first? → Process Management → Processes
→ CPU Scheduling → FCFS / SJF / Round Robin → Quiz → Performance → Weak Topics
→ Next Recommended Topic
```

## Architecture

```
        STUDENT
           │
           ▼
   React Frontend  (frontend/)
           │  REST (fetch)
           ▼
  Python FastAPI Backend  (backend/main.py)
           │
   ┌───────┼────────────┐
   ▼       ▼             ▼
AI Engine  Algorithm     Database
(ai_engine.py)  Engine    (database.py — SQLite by default,
   │       (graph_engine.py:      MongoDB-ready)
   │        BFS/DFS,
   │        quiz_engine.py,
   │        recommendation_engine.py)
   ▼
Knowledge Base (knowledge_base.py + data/*.json)
```

| Diagram box | File |
|---|---|
| AI Engine (NLP/ML/RAG) | `backend/ai_engine.py` |
| Algorithm Engine (BFS/DFS) | `backend/graph_engine.py` |
| Recommendation | `backend/recommendation_engine.py` |
| Database | `backend/database.py` (SQLite; MongoDB code included, commented) |
| Knowledge Base | `backend/knowledge_base.py` + `backend/data/` |

## What's real vs. what's a stub

This runs fully end-to-end with **no API keys and no internet** required:

- ✅ **Real**: FastAPI REST API, BFS/DFS prerequisite graph traversal, topological
  sort study-path generation, quiz grading, SQLite persistence, weak-topic
  detection, next-topic recommendation logic, full React UI.
- 🔧 **Stubbed (by design, swap-in ready)**: `ai_engine.py`'s topic explanations are
  rule-based/templated rather than calling a real LLM. The file has clear comments
  showing exactly how to plug in a real Anthropic/OpenAI call for true RAG-based
  explanations — it's a 10-line change once you have an API key.
- 🔧 **Stubbed**: Storage defaults to SQLite (zero setup). A parallel MongoDB
  implementation is sketched (commented) in `database.py` if you want to match the
  diagram exactly — just uncomment, `pip install motor`, and point it at your
  Mongo instance.

Currently only one subject/topic chain is seeded (**Operating System → CPU
Scheduling → FCFS/SJF/Round Robin**) as a working example — add more subjects by
editing `backend/data/topics.json` and `backend/data/quiz_bank.json` (see below).

## Running it

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 2. Frontend

```bash
cd frontend
npm install
npm start
```

Opens at http://localhost:3000. It talks to the backend at `http://localhost:8000`
by default — override with a `.env` file containing `REACT_APP_API_URL=...` if
your backend runs elsewhere.

## API Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/subjects` | List subjects |
| GET | `/topics` | List all topics |
| GET | `/topics/{id}/path` | BFS/DFS study order (prerequisites → target) |
| GET | `/topics/{id}/content` | AI-generated (currently rule-based) explanation |
| GET | `/topics/{id}/next` | Child topics in the DAG |
| GET | `/quiz/{id}` | Quiz questions (answers stripped) |
| POST | `/quiz/{id}/submit` | Grade a quiz, persist the attempt |
| GET | `/student/{id}/performance` | Score history + weak topics |
| GET | `/student/{id}/recommend` | Next recommended topic |

## Adding more topics

Edit `backend/data/topics.json`:

```json
"new_topic_id": {
  "id": "new_topic_id",
  "name": "Display Name",
  "prerequisites": ["some_existing_topic_id"],
  "content": "Explanation shown to the student.",
  "estimated_minutes": 15
}
```

Then add matching quiz questions with the same key in `backend/data/quiz_bank.json`.
The BFS/DFS engine and recommendation logic pick up new topics automatically —
no code changes needed.

## Next steps to make this production-grade

1. Swap `ai_engine.py`'s stub for a real LLM call (Anthropic/OpenAI) doing RAG over
   `knowledge_base.py` — the comment block in that file shows exactly how.
2. Swap SQLite for MongoDB using the commented code in `database.py` if you need
   multi-server deployments.
3. Add real authentication instead of the hardcoded `demo_student` id in
   `frontend/src/App.js`.
4. Expand `topics.json` / `quiz_bank.json` with more subjects (Data Structures,
   DBMS, Networks, etc.) — the graph/recommendation engines are subject-agnostic.
