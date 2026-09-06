# CognitiveAI

## Modular AI Decision Intelligence Platform

The Cognitive AI Decision Intelligence Platform is a modular AI system designed to solve real-world business problems across multiple industries using a unified architecture.

## AI Decision Intelligence Platform

Cognitive AI is a production-oriented AI platform designed to combine

machine learning, semantic retrieval, RAG, agentic workflows,

risk intelligence, and AI infrastructure into a reusable system.

## Target Domains

* Logistics & Supply Chain
* E-commerce & Retail
* Enterprise Knowledge
* Finance & Risk

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
* Established a reusable architecture for future **RAG, Agentic AI, and Multi-Agent workflows**.

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

---

## Dataset Collection

CognitiveAI uses domain-specific datasets across four areas: **Logistics & Supply Chain, E-commerce & Retail, Enterprise Knowledge, and Finance & Risk**.

Each domain contains a **clean/true reference dataset** from an authoritative source and additional **noisy domain data** for heterogeneous ingestion testing.

### Domains

* **Logistics & Supply Chain** — DataCo Smart Supply Chain Dataset
* **E-commerce & Retail** — 2022 Annual Retail Trade Survey (ARTS)
* **Enterprise Knowledge** — NIST Cybersecurity Framework (CSF) 2.0
* **Finance & Risk** — Federal Reserve H.8: Assets and Liabilities of Commercial Banks

### Data Sources

* Logistics: [DataCo Smart Supply Chain Dataset](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis)
* E-commerce: [U.S. Census Bureau — Annual Retail Trade Survey](https://www.census.gov/programs-surveys/arts.html)
* Enterprise: [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
* Finance: [Federal Reserve H.8 Data](https://www.federalreserve.gov/datadownload/Download.aspx?rel=H8)