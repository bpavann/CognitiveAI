import logfire
from app.agents.state import AgentState
from app.services.llmgateway.client import portkey_client

def coding_agent_node(state: AgentState):
    """
    Handles coding-related requests.
    The Coding Agent understands the programming task
    and generates an appropriate coding solution.
    """
    query = state["current_query"]
    with logfire.span("💻 Coding Agent"):
        logfire.info(f"Processing coding request: {query}")
        prompt = f"""
        You are a Senior Software Engineer and Coding Agent.
        Your responsibility is to solve programming-related requests.
        CODING 
            - Writing code 
            - Debugging code 
            - Explaining code 
            - Code review 
            - Programming questions 
            - Creating APIs, scripts, functions, classes, etc. 
            - Software engineering implementation tasks

        USER CODING REQUEST:
        {query}

        Instructions:
        - Understand the programming requirement.
        - Provide correct and production-quality code.
        - Explain the important parts of the solution.
        - Handle errors and edge cases when appropriate.
        - Do not use knowledge retrieval unless explicitly required.
        - Do not pretend to execute code.
        """
        try:
            response = portkey_client.chat.completions.create(messages=[{"role": "user","content": prompt}],temperature=0.1)
            content = response.choices[0].message.content
            logfire.info("Coding solution generated successfully.")
            return {
                "final_answer": content,
                "status": "Coding solution generated.",
                "plan": state["plan"] + ["Coding Solution Generated"]
            }
        except Exception as e:
            logfire.error(f"Coding Agent failed: {e}")
            raise e