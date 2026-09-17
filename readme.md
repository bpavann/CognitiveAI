# CognitiveAI

## Modular AI Decision Intelligence Platform

**CognitiveAI** is a modular AI decision intelligence platform engineered to combine **agentic reasoning, enterprise RAG, LLM infrastructure, AI security, and observability** within a single extensible architecture.

The system is designed around a controlled AI execution pipeline rather than a simple chatbot. User requests are classified, routed through appropriate reasoning paths, grounded against enterprise knowledge when required, and validated through multiple security and quality controls before a response is returned.

The current knowledge domain is **NIST cybersecurity and AI risk management**, providing a concrete enterprise knowledge base for validating the architecture.

---

## Core Capabilities

### Agentic Decision Workflow

CognitiveAI uses **LangGraph** to orchestrate stateful AI execution and route requests according to their intent.

The current reasoning paths include:

* **Conversational reasoning** for general user interactions.
* **Research reasoning** for knowledge-intensive queries requiring enterprise retrieval.
* **Coding reasoning** for programming and technical requests.
* Stateful execution containing the user query, routing decision, retrieved knowledge, execution plan, and final response.

This separates **request routing from knowledge retrieval and response generation**, allowing additional specialized agents or decision workflows to be introduced without redesigning the entire platform.

---

## Enterprise RAG

The research workflow implements a multi-stage retrieval pipeline rather than passing raw vector-search results directly to the LLM.

```text
User Query
    ↓
Semantic Retrieval
    ↓
Metadata Filtering
    ↓
Security Validation
    ↓
Relevance Filtering
    ↓
FlashRank Reranking
    ↓
PII Masking
    ↓
Untrusted Context
    ↓
LLM Reasoning
    ↓
Grounding Validation
```

The retrieval layer provides:

* Semantic search over the CognitiveAI knowledge base using vector embeddings.
* **Qdrant** for persistent vector storage and similarity search.
* Metadata-aware retrieval for controlling the knowledge scope.
* **FlashRank** reranking to improve the ordering of retrieved candidates.
* Relevance thresholds to prevent weak retrieval results from reaching the reasoning layer.
* Retrieval-level inspection for indirect prompt injection.
* PII sanitization before retrieved content enters the LLM context.
* Explicit **untrusted-context boundaries** so retrieved documents are treated as information rather than instructions.

This creates a separation between **retrieved knowledge and executable instructions**, which is important when building RAG systems that consume external or enterprise documents.

---

## NIST Knowledge Intelligence

The initial CognitiveAI knowledge domain is built from authoritative **NIST publications** covering:

* NIST Cybersecurity Framework (CSF)
* NIST AI Risk Management Framework (AI RMF)
* Cybersecurity risk management
* AI risk management
* Zero Trust Architecture
* Secure software development
* Related NIST technical publications

The knowledge collection includes structured and unstructured resources such as **PDF, HTML, and XLSX documents**.

The NIST dataset serves as the first enterprise knowledge domain while the underlying retrieval and orchestration architecture remains domain-agnostic.

**Official Source:** [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

## AI Security Architecture

Security is treated as a pipeline-level concern rather than a single moderation step.

### Input Layer

User requests pass through:

* Self-check validation
* Jailbreak detection
* Prompt injection detection
* PII detection and masking

### Retrieval Layer

Retrieved documents are inspected before being exposed to the reasoning model:

* Indirect prompt injection detection
* Retrieval relevance validation
* PII masking
* Untrusted-context marking

### Generation Layer

Generated responses are validated through:

* Grounding checks against retrieved knowledge
* Output PII detection and masking
* NeMo Guardrails output validation

This provides multiple control points across the lifecycle of an AI request:

```text
Input
  ↓
Validate
  ↓
Retrieve
  ↓
Secure Context
  ↓
Generate
  ↓
Validate
  ↓
Return
```

The architecture is designed so that security controls can evolve independently from the underlying agent and retrieval logic.

---

## LLM Infrastructure

CognitiveAI uses **Portkey AI** as an LLM gateway between application services and model providers.

The gateway provides:

* Centralized model access.
* Provider abstraction.
* LLM routing.
* Retry and fallback behavior.
* Response caching.
* Cache-hit and cache-miss visibility.
* Request metadata for feature-level tracking.

A dedicated LLM service layer keeps application logic independent from individual model providers and allows the same infrastructure to support conversational, RAG, and agentic workloads.

---

## Observability

AI systems require visibility beyond traditional application logs. CognitiveAI therefore separates **application observability from AI workflow tracing**.

### Logfire

Used for:

* FastAPI instrumentation
* Request-level tracing
* Custom execution spans
* Retrieval and guardrail events
* AI pipeline diagnostics
* Error tracking

### LangSmith

Used for:

* LangChain execution tracing
* LLM workflow visibility
* Agent execution analysis
* RAG pipeline inspection

### Portkey

Used for:

* LLM request metadata
* Provider-level monitoring
* Cache-status visibility
* Gateway-level execution information

Together these layers provide visibility from the **API request through agent execution, retrieval, LLM generation, and security validation**.

---

## Application Interface

A lightweight **Streamlit interface** provides the user-facing interaction layer.

The interface supports:

* Conversational interaction with CognitiveAI.
* Persistent conversation state.
* Backend API communication.
* Separation between presentation, orchestration, and AI services.

The frontend is intentionally lightweight; the core intelligence remains exposed through the backend API so the same AI services can be consumed by other interfaces or applications.

---

## Backend API

The platform exposes its AI capabilities through **FastAPI**.

The backend provides:

* REST-based AI interaction.
* Pydantic request and response validation.
* Swagger/OpenAPI documentation.
* LangGraph workflow execution.
* Structured error handling.
* Integration with retrieval, LLM, security, and observability services.

The API acts as the execution boundary between the user-facing application and the CognitiveAI intelligence layer.

---

## System Architecture

```text
                         ┌──────────────────────┐
                         │        User          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Input Security     │
                         │ PII / Jailbreak /    │
                         │ Prompt Injection     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  LangGraph Router    │
                         └───────┬──┬──┬─────────┘
                                 │  │  │
                    ┌────────────┘  │  └────────────┐
                    ▼               ▼               ▼
             Conversational      Research         Coding
                                    │
                                    ▼
                              ┌────────────┐
                              │   Qdrant   │
                              │  Retrieval │
                              └─────┬──────┘
                                    │
                                    ▼
                              ┌────────────┐
                              │  Security  │
                              │ + Relevance│
                              └─────┬──────┘
                                    │
                                    ▼
                              ┌────────────┐
                              │ FlashRank  │
                              │ Reranking  │
                              └─────┬──────┘
                                    │
                                    ▼
                              ┌────────────┐
                              │  Secure    │
                              │  Context   │
                              └─────┬──────┘
                                    │
                                    ▼
                              ┌────────────┐
                              │    LLM     │
                              │ Reasoning  │
                              └─────┬──────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Grounding + Output   │
                         │ Security Validation  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Final Response     │
                         └──────────────────────┘
```

---

## Engineering Characteristics

CognitiveAI is designed around several engineering principles:

* **Modularity** — retrieval, orchestration, LLM infrastructure, security, and observability remain independently extensible.

* **Provider abstraction** — LLM access is mediated through a gateway rather than tightly coupling the application to a single provider.

* **Knowledge grounding** — research responses are generated using retrieved enterprise context rather than relying exclusively on model parametric knowledge.

* **Defense in depth** — security controls operate at multiple stages of the AI pipeline.

* **Stateful orchestration** — LangGraph maintains structured execution state across routing, retrieval, reasoning, and response generation.

* **Traceability** — application and AI execution can be inspected through dedicated observability systems.

* **Domain extensibility** — NIST is the current knowledge domain, while the retrieval and orchestration architecture can support additional enterprise datasets.

---

## Technology Stack

| Layer               | Technology            |
| ------------------- | --------------------- |
| Language            | Python                |
| User Interface      | Streamlit             |
| API                 | FastAPI               |
| Agent Orchestration | LangGraph             |
| LLM Framework       | LangChain             |
| LLM Gateway         | Portkey AI            |
| Vector Database     | Qdrant                |
| Reranking           | FlashRank             |
| Embeddings          | Sentence Transformers |
| AI Guardrails       | NeMo Guardrails       |
| PII Protection      | Microsoft Presidio    |
| Observability       | Logfire, LangSmith    |
| Package Management  | uv                    |

---

## Current Development Stage

The core CognitiveAI architecture is operational across the major AI-system layers:

**RAG → Agentic Orchestration → LLM Infrastructure → Security → Observability → API → Interface**

The remaining engineering work is focused primarily on **agent action validation, systematic evaluation/testing, production hardening, deployment, and final project documentation**.

CognitiveAI is therefore being developed as an **AI systems engineering platform**, with NIST serving as the initial enterprise knowledge domain rather than as the sole purpose of the system.
