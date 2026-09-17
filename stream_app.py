import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CognitiveAI",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 CognitiveAI")
st.caption("**NIST-Focused Knowledge-Driven Multi-Agent AI System**")
st.markdown(
    """
    CognitiveAI provides knowledge-grounded answers across:
    **NIST Cybersecurity Framework • NIST AI RMF • Generative AI Risk
    • Zero Trust • Secure Software Development**
    """
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "BPK-1"


# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # Display CognitiveAI metadata for assistant messages
        if message["role"] == "assistant":

            if message.get("status"):
                st.caption(f"Status: {message['status']}")

            if message.get("plan"):
                with st.expander("🧠 Execution Plan"):
                    for step in message["plan"]:
                        st.write(f"• {step}")

            if message.get("documents"):
                with st.expander("📚 Retrieved documents"):
                    for index, document in enumerate(message["documents"],start=1):
                        if isinstance(document, dict):
                            st.markdown(f"**Documents {index}**")
                            if document.get("documents"):
                                st.write(f"Documents: {document['document']}")

                            if document.get("page"):
                                st.write(f"Page: {document['page']}")

                            if document.get("rerank_score") is not None:
                                st.write(
                                    f"Rerank score: "
                                    f"{document['rerank_score']:.4f}"
                                )
                            st.write(document.get("content", ""))
                        else:
                            st.write(document)

# Chat Input
prompt = st.chat_input(
    "Ask CognitiveAI anything..."
)

if prompt:
    # Display user message
    st.session_state.messages.append({"role": "user","content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI
    try:
        response = httpx.post(f"{API_URL}/chat",json={"message": prompt, "thread_id": st.session_state.thread_id},timeout=60)
        response.raise_for_status()
        data = response.json()
        assistant_response =data.get("answer", "No response was generated.")
        status = data.get("status", "")
        plan = data.get("thought_process",[])
        documents = data.get("documents",[])

    except httpx.HTTPStatusError as error:
        assistant_response = (f"API error: {error.response.status_code}")
        status = "API error"
        plan = []
        documents = []

    except httpx.RequestError as error:
        assistant_response = (f"Backend connection failed: {error}")
        status = "Connection error"
        plan = []
        documents = []

    except Exception as error:
        assistant_response = (f"Unexpected error: {error}")
        status = "Unexpected error"
        plan = []
        documents = []

    # Display Assistant Response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        if status:
            st.caption(f"Status: {status}")
            
        if plan:
            with st.expander("🧠 Execution Plan"):
                for step in plan:
                    st.write(f"• {step}")

        if documents:
            with st.expander("📚 Retrieved Sources"):
                for index, document in enumerate(documents,start=1):
                    if isinstance(document, dict):
                        st.markdown(f"**Source {index}**")

                        if document.get("document"):
                            st.write(f"Document: {document['document']}")

                        if document.get("page"):
                            st.write(f"Page: {document['page']}")

                        if document.get("rerank_score") is not None:
                            st.write(
                                f"Rerank score: "
                                f"{document['rerank_score']:.4f}"
                            )

                        st.write(document.get("content", ""))

                    else:
                        st.write(document)
    
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
            "status": status,
            "plan": plan,
            "documents": documents,
        }
    )