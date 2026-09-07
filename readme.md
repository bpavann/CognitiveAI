# CognitiveAI

## Modular AI Decision Intelligence Platform

The CognitiveAI Decision Intelligence Platform is a modular AI system designed to solve real-world business problems using a unified architecture.

## AI Decision Intelligence Platform

CognitiveAI is a production-oriented AI platform designed to combine machine learning, semantic retrieval, RAG, agentic workflows, risk intelligence, and AI infrastructure into a reusable system.

---

## Dataset

### NIST Knowledge Collection

A curated collection of official NIST resources covering cybersecurity, AI risk management, Zero Trust Architecture, and secure software development. The collection includes PDF, HTML, and XLSX resources gathered from authoritative NIST publications.

**Official Source:** [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

### Frontend — Streamlit

* Built a lightweight **Streamlit-based AI interface** for interacting with the CognitiveAI platform.
* Implemented **chat-based interaction** with conversation state using Streamlit session state.
* Integrated the frontend with the backend through **HTTP API communication**.
* Separated the frontend layer from backend and AI services.

### Backend — FastAPI

* Built a modular **FastAPI backend** for exposing CognitiveAI services through REST APIs.
* Implemented health monitoring through the `GET /api/health` endpoint.
* Implemented AI interaction through the `POST /api/chat` endpoint.
* Added **Pydantic request and response models** for API validation.
* Enabled **Swagger/OpenAPI documentation** through FastAPI.

### LLM Gateway — Portkey AI

* Integrated a centralized **Portkey AI LLM Gateway** for model communication.
* Implemented a reusable `get_llm()` interface for creating Portkey-backed LangChain LLM clients.
* Configured **LLM routing, fallback handling, retry behavior, and caching** through Portkey.
* Added feature-level metadata to LLM requests for tracking and observability.
* Implemented Portkey **cache-status extraction** for monitoring cache hits and misses.
* Decoupled the application from direct dependency on individual LLM providers.

### LLM Service Layer

* Created a dedicated **LLM service layer** between FastAPI APIs and the LLM Gateway.
* Separated application-level AI logic from Portkey configuration.
* Implemented asynchronous LLM invocation using **LangChain**.
* Established a reusable architecture for **RAG, Agentic AI, and Multi-Agent workflows**.

### Observability

* Integrated **Logfire** for application and AI-service observability.
* Added FastAPI request instrumentation and custom application spans.
* Added LLM generation tracing for monitoring AI execution.
* Integrated **LangSmith** for LangChain and LLM tracing.
* Added LLM cache-status logging for monitoring Portkey responses.
* Established separate observability layers for **application execution and AI workflows**.

---

## Technology Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **LLM Framework:** LangChain
* **LLM Gateway:** Portkey AI
* **Observability:** Logfire, LangSmith
* **Environment & Package Management:** uv
* **Language:** Python
