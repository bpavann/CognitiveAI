from app.agents.graph import cognitive_ai_agent


def test_query(query: str):

    state = {
        "messages": [
            {
                "role": "user",
                "content": query
            }
        ],
        "current_query": "",
        "agent_type": "",
        "documents": [],
        "plan": [],
        "status": "",
        "final_answer": "",
    }

    result = cognitive_ai_agent.invoke(
        state,
        config={
            "configurable": {
                "thread_id": "test-1"
            }
        }
    )

    print("\n" + "=" * 70)
    print("USER QUERY:", query)
    print("AGENT:", result.get("agent_type"))
    print("QUERY:", result.get("current_query"))
    print("STATUS:", result.get("status"))
    print("PLAN:", result.get("plan"))
    print("DOCUMENTS:", len(result.get("documents", [])))
    print("ANSWER:", result.get("final_answer"))
    print("=" * 70)


if __name__ == "__main__":

    queries = [
        "Hi, how are you?",
        "What are the five functions of NIST CSF 2.0?",
        "Write a Python function that validates a JSON file.",
        "What is Zero Trust Architecture?",
    ]

    for query in queries:
        test_query(query)