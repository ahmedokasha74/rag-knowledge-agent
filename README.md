# RAG Knowledge Agent

A portfolio-grade Retrieval-Augmented Generation (RAG) project focused on building and evaluating enterprise knowledge retrieval systems.

The project uses a fictional SaaS company, Cloudify, as its enterprise knowledge base and progressively explores different RAG architectures and techniques. MCP is not the current focus of this repository.

## Current Stage

### Phase 1 — Basic RAG

The current implementation provides a complete standalone RAG pipeline for the Cloudify knowledge base:

```text
Documents
  → Reader
  → Chunking
  → Embeddings
  → Qdrant
  → Retrieval
  → Context Augmentation
  → LLM Generation
```

This is the currently implemented stage.

## Implemented Features

- Enterprise knowledge base using Markdown documents
- Markdown document ingestion
- Recursive Character, Token, and Semantic chunking
- Embedding provider abstraction
- LLM provider abstraction
- Qdrant vector database
- Ingestion Controller
- Retrieval Controller
- Basic RAG Pipeline
- Similarity score threshold filtering
- RAG query testing

## Knowledge Base

Cloudify documentation covers Refund Policy, Subscription Policy, Billing, SLA, Support, Security, Privacy, Data Retention, API Usage, Incident Response, Enterprise Plan, Account Management, Acceptable Use, and Onboarding.

The documents contain relationships across policies and are intentionally structured to support future GraphRAG and Hybrid RAG experiments.

## Architecture

```text
                    ┌──────────────────┐
                    │  Cloudify Docs   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Reader      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Chunking      │
                    │ Recursive/Token/ │
                    │    Semantic      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Embeddings    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Qdrant      │
                    └────────┬─────────┘
                             │
                        User Query
                             │
                             ▼
                    ┌──────────────────┐
                    │    Retrieval     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Context Augment. │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  LLM Generation  │
                    └────────┬─────────┘
                             │
                             ▼
                           Answer
```

## Technology Stack

- Python
- LangChain
- Qdrant
- Cohere Embeddings
- Groq
- Pydantic Settings
- uv
- WSL / Linux

## Project Structure

```text
src/
├── controllers/
│   ├── reader.py
│   ├── chunking/
│   ├── ingestion/
│   ├── retrieval/
│   └── rag/
├── helpers/
├── models/
├── stores/
│   ├── llm/
│   └── vectordb/
└── tests/

data/
└── documents/
    └── Cloudify knowledge base
```

## Roadmap

### Phase 1 — Basic RAG

- [x] Document ingestion
- [x] Chunking
- [x] Embeddings
- [x] Vector database
- [x] Similarity retrieval
- [x] Context augmentation
- [x] LLM generation
- [x] Similarity score threshold

### Phase 2 — Chunking Experiments

- [x] Recursive chunking
- [x] Token chunking
- [x] Semantic chunking
- [ ] Compare retrieval performance
- [ ] Analyze chunking impact

### Phase 3 — RAG Evaluation

- [ ] Retrieval evaluation
- [ ] Similarity / ranking metrics
- [ ] LLM-based relevance evaluation
- [ ] Ragas evaluation
- [ ] Compare different RAG configurations

### Phase 4 — GraphRAG

- [ ] Neo4j knowledge graph
- [ ] Entity extraction
- [ ] Relationship extraction
- [ ] Graph-based retrieval
- [ ] GraphRAG pipeline

### Phase 5 — Hybrid GraphRAG

- [ ] Qdrant vector retrieval
- [ ] Neo4j graph retrieval
- [ ] Hybrid retrieval strategy
- [ ] Context fusion
- [ ] Hybrid RAG evaluation

### Phase 6 — Agentic RAG

- [ ] Query analysis
- [ ] Retrieval planning
- [ ] Tool-based retrieval
- [ ] Iterative retrieval
- [ ] Agentic RAG evaluation

## Future MCP Integration

MCP is intentionally kept outside this repository. After the RAG development stages are complete, this project will serve as a RAG/backend capability for a separate MCP-based enterprise agent.

```text
rag-knowledge-agent
        │
        │ RAG Backend
        ▼
┌─────────────────────────┐
│  MCP Enterprise Agent   │
│                         │
│  MCP Host / Client      │
│  MCP Servers            │
│  Enterprise Tools       │
└─────────────────────────┘
```

The future MCP repository will expose RAG capabilities and other enterprise tools through the Model Context Protocol.

## Goal

The goal is to progressively build a production-oriented RAG system while experimenting with retrieval, chunking, evaluation, graph-based retrieval, hybrid architectures, and agentic workflows.

The long-term project will evolve from Basic RAG into GraphRAG, Hybrid GraphRAG, and Agentic RAG. MCP will be demonstrated separately in another repository.
