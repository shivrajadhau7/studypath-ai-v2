"""
graph_engine.py
----------------
The "Algorithm Engine" box in the architecture diagram.

Builds a prerequisite DAG from the knowledge base and uses BFS / DFS +
topological sort to answer:

    "What should I know first before I can learn X?"

Example (CPU Scheduling):
    CPU Scheduling -> Processes -> Process Management
So the correct STUDY ORDER (topological order) is:
    Process Management -> Processes -> CPU Scheduling
"""

from collections import deque, defaultdict
from knowledge_base import TOPICS


def _build_graph():
    """adjacency[a] = [b, c] means a is a prerequisite OF b and c."""
    adjacency = defaultdict(list)
    indegree = defaultdict(int)
    for topic_id, topic in TOPICS.items():
        indegree.setdefault(topic_id, 0)
        for prereq in topic["prerequisites"]:
            adjacency[prereq].append(topic_id)
            indegree[topic_id] += 1
    return adjacency, indegree


def get_direct_prerequisites(topic_id):
    topic = TOPICS.get(topic_id)
    if not topic:
        return []
    return topic["prerequisites"]


def bfs_prerequisite_chain(topic_id):
    """
    BFS backwards through prerequisites to collect every ancestor topic
    needed before `topic_id` can be studied.
    """
    visited = set()
    queue = deque([topic_id])
    chain = []
    while queue:
        current = queue.popleft()
        for prereq in TOPICS.get(current, {}).get("prerequisites", []):
            if prereq not in visited:
                visited.add(prereq)
                chain.append(prereq)
                queue.append(prereq)
    return chain


def dfs_topological_order(topic_id):
    """
    DFS-based topological sort restricted to the ancestors of `topic_id`
    (plus the topic itself), returning the correct STUDY ORDER — earliest
    foundational topic first.
    """
    visited = set()
    order = []

    def visit(node):
        if node in visited or node not in TOPICS:
            return
        visited.add(node)
        for prereq in TOPICS[node]["prerequisites"]:
            visit(prereq)
        order.append(node)

    visit(topic_id)
    return order  # already root-first because we append AFTER visiting prereqs


def get_learning_path(topic_id):
    """Full response used by the /topics/{id}/path endpoint."""
    if topic_id not in TOPICS:
        return None
    order = dfs_topological_order(topic_id)
    return [
        {
            "id": t,
            "name": TOPICS[t]["name"],
            "estimated_minutes": TOPICS[t]["estimated_minutes"],
            "is_target": t == topic_id,
        }
        for t in order
    ]


def get_next_topics(topic_id):
    """Children in the DAG — e.g. children of cpu_scheduling = FCFS, SJF, RR."""
    adjacency, _ = _build_graph()
    children = adjacency.get(topic_id, [])
    return [{"id": c, "name": TOPICS[c]["name"]} for c in children]
