# CognitiveAI

## Modular AI Decision Intelligence Platform

The **CognitiveAI Decision Intelligence Platform** is a modular, production-oriented AI system designed to solve real-world business and knowledge-intensive problems using a unified AI architecture.

CognitiveAI combines **LLMs, semantic retrieval, RAG, agentic workflows, AI security guardrails, observability, and enterprise knowledge** into a reusable AI platform.

The current implementation focuses on **NIST cybersecurity and AI risk management knowledge**, while the architecture is designed to support additional enterprise knowledge domains.

---

## AI Decision Intelligence Platform

CognitiveAI provides a controlled AI workflow that:

* Accepts natural-language user requests through an interactive interface and API.

* Classifies and routes requests through an **agentic reasoning workflow**.

* Retrieves relevant enterprise knowledge using **semantic search and RAG**.

* Uses **Qdrant vector search and FlashRank reranking** to improve knowledge retrieval.

* Applies security controls to both user inputs and retrieved knowledge.

* Treats retrieved information as **untrusted context** rather than executable instructions.

* Generates responses using configurable LLM infrastructure.

* Validates generated answers against retrieved knowledge to improve grounding.

* Detects and masks sensitive information before returning responses.

* Provides application and LLM observability through **Logfire and LangSmith**.

* Uses **Portkey AI** as an LLM gateway for routing, retries, fallback handling, and caching.

---

## Knowledge Base

### NIST Knowledge Collection

The current CognitiveAI knowledge base contains curated official NIST resources covering:

* NIST Cybersecurity Framework (CSF)
* NIST AI Risk Management Framework (AI RMF)
* Cybersecurity risk management
* AI risk management
* Zero Trust Architecture
* Secure software development
* Related NIST technical publications

The collection includes **PDF, HTML, and XLSX resources** gathered from authoritative NIST publications.


**Official Source:** [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

## RAG & Knowledge Intelligence

* Implemented a complete **document ingestion and semantic retrieval pipeline**.

* Added support for multiple enterprise document formats.

* Implemented document cleaning, metadata extraction, and chunking.

* Generated embeddings for semantic knowledge retrieval.

* Integrated **Qdrant** as the vector database.

* Implemented metadata-based retrieval filtering.

* Added **FlashRank reranking** to improve retrieved-context relevance.

* Added retrieval relevance validation to reduce low-quality context.

* Added retrieval security checks to detect suspicious or instruction-like content.

* Added PII masking for retrieved knowledge.

* Added untrusted-context handling to ensure retrieved documents are treated as data rather than instructions.

---

## Agentic AI

* Implemented a **LangGraph-based agentic workflow**.

* Added intelligent request routing between conversational, research, and coding workflows.

* Connected the research workflow directly to the CognitiveAI knowledge base.

* Maintained execution state across the AI workflow.

* Added structured execution information for improved traceability.

* Designed the architecture to support future enterprise AI agents and decision-intelligence workflows.

---

## AI Security & Guardrails

CognitiveAI includes security controls across the AI pipeline.

### Input Protection

* Self-checking of user requests.

* Jailbreak detection.

* Prompt injection detection.

* PII detection and masking.

### Retrieval Protection

* Indirect prompt injection detection.

* Retrieval relevance validation.

* Retrieved-content PII masking.

* Untrusted-context protection.

### Output Protection

* Output PII detection and masking.

* Grounding validation against retrieved knowledge.

* Output safety validation.

### Agent Protection

* Agent action validation is planned for controlling tool and action execution.

---

## Frontend

* Built a lightweight **Streamlit-based chat interface**.

* Supports conversational interaction with CognitiveAI.

* Maintains conversation state.

* Communicates with the backend through HTTP APIs.

* Keeps the user interface separated from the AI and backend services.

---

## Backend

* Built a **FastAPI backend** for CognitiveAI services.

* Implemented chat interaction through REST APIs.

* Added request and response validation using **Pydantic**.

* Added Swagger/OpenAPI API documentation.

* Integrated the LangGraph AI workflow with the backend.

* Added structured error handling for AI execution and security failures.

---

## LLM Infrastructure

* Integrated **Portkey AI** as a centralized LLM gateway.

* Implemented reusable LLM configuration through LangChain.

* Added LLM routing and provider abstraction.

* Added retry and fallback handling.

* Added semantic/application-level caching.

* Added cache-status monitoring.

* Added feature-level metadata for LLM request tracking.

* Decoupled CognitiveAI from direct dependency on a single LLM provider.

---

## Observability

* Integrated **Logfire** for application and AI-service observability.

* Added FastAPI request instrumentation.

* Added custom execution spans and structured logging.

* Integrated **LangSmith** for LangChain and LLM tracing.

* Added LLM cache-status monitoring.

* Added logging for guardrail and retrieval security events.

* Added execution visibility across the CognitiveAI pipeline.

---

## Technology Stack

* **Language:** Python

* **Frontend:** Streamlit

* **Backend:** FastAPI

* **AI Orchestration:** LangGraph

* **LLM Framework:** LangChain

* **LLM Gateway:** Portkey AI

* **Vector Database:** Qdrant

* **Reranking:** FlashRank

* **Embeddings:** Sentence Transformers

* **Guardrails:** NeMo Guardrails

* **PII Protection:** Microsoft Presidio

* **Observability:** Logfire, LangSmith

* **Environment & Package Management:** uv

---
