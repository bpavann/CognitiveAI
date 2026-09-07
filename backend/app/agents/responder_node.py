import logfire
from app.agents.state import AgentState
from app.services.llmgateway.client import portkey_client,extract_cache_status

def generate_node(state: AgentState):
    """
    Generates the final response.

    Handles:
        - CONVERSATIONAL requests
        - RESEARCH requests
        - Temporary CODING fallback

    Research requests use retrieved Qdrant context.
    """

    agent_type = state["agent_type"]

    history_str = ""

    for msg in state["messages"][:-1]:

        role = (
            "User"
            if msg["role"] == "user"
            else "Assistant"
        )

        history_str += (
            f"{role}: {msg['content']}\n"
        )

    user_msg = (
        state["messages"][-1]["content"]
        if state["messages"]
        else ""
    )

    # Conversational
    if agent_type == "CONVERSATIONAL":
        logfire.info("Generating conversational response.")
        prompt = f"""
        You are a friendly and helpful Enterprise AI Assistant.

        Answer the user's latest message naturally using the
        conversation history when useful.

        CONVERSATION HISTORY:
        {history_str}

        LATEST USER MESSAGE:
        "{user_msg}"
        """

    # Research
    elif agent_type == "RESEARCH":
        logfire.info("Generating research response using RAG context.")
        max_context_chars = 25000
        full_context = ""
        for doc in state.get("documents", []):
            if (len(full_context) + len(doc)< max_context_chars):
                full_context += (doc + "\n\n")
            else:
                logfire.warning("Context truncated.")
                break

        prompt = f"""
        You are a Senior Technical Architect.

        Answer the user's question using the provided
        technical context.

        Use the context as the primary source of truth.

        If the context does not contain enough information,
        clearly state that instead of inventing facts.

        TECHNICAL CONTEXT:
        {full_context}

        CONVERSATION HISTORY:
        {history_str}

        USER QUESTION:
        "{user_msg}"
        """

    # Coding
    else:
        logfire.info("Generating temporary coding response.")
        prompt = f"""
        You are a senior software engineer.

        Answer the user's coding question clearly and
        provide correct code when required.

        CONVERSATION HISTORY:
        {history_str}

        USER QUESTION:
        "{user_msg}"
        """

    # LLM Generation
    with logfire.span("✍️ LLM Synthesis"):

        try:
            response = portkey_client.chat.completions.create(messages=[{"role": "user","content": prompt}],temperature=0.1)

            content = (response.choices[0].message.content)

            cache_status = extract_cache_status(response)

            is_cache_hit = (cache_status == "HIT")
            if is_cache_hit:
                logfire.info("⚡ Portkey cache hit.")
                plan_update = (state["plan"] + ["Cache: Hit ⚡"])
                status = ("Cache hit — instant response.")
            else:
                logfire.info("✅ Response generated.")
                plan_update = state["plan"]
                status = ("Response generated.")
            return {
                "final_answer": content,
                "status": status,
                "plan": plan_update,
                "messages": [
                    {
                        "role": "assistant",
                        "content": content,
                    }
                ],
            }
        except Exception as e:
            logfire.error(f"LLM Generation failed: {e}")
            raise