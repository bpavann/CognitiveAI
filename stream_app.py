import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="CognitiveAI",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 CognitiveAI")
st.caption(
    "Modular Multi-Agent AI Orchestration Platform"
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
        response = httpx.post(
            f"{API_URL}/api/chat",
            json={
                "message": prompt
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        assistant_response = data["response"]

    except httpx.HTTPStatusError as error:
        assistant_response = (f"API error: {error.response.status_code}")

    except httpx.RequestError as error:
        assistant_response = (f"Backend connection failed: {error}")

    except Exception as error:
        assistant_response = (f"Unexpected error: {error}")

    # Display Assistant Response
    st.session_state.messages.append({"role": "assistant","content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
