# MCP Knowledge Agent

A portfolio-grade Generative AI project exploring enterprise knowledge workflows and the Model Context Protocol (MCP).

## Current Stage

Phase 0 / Standalone RAG

The project currently implements a standalone Retrieval-Augmented Generation (RAG) pipeline for the Cloudify knowledge base.

Pipeline:

Documents
→ Reader
→ Chunking
→ Embeddings
→ Qdrant
→ Retrieval
→ Context Augmentation
→ LLM Generation

## Implemented Components

- Cloudify enterprise knowledge base
- Markdown document reader
- Recursive, Token, and Semantic chunking
- Embedding provider abstraction
- LLM provider abstraction
- Qdrant vector database
- Ingestion Controller
- Retrieval Controller
- RAG Pipeline
- Similarity score threshold filtering
- RAG tests

## Knowledge Base

The current knowledge base contains Cloudify policies and operational documentation covering areas such as:

- Refunds
- Subscriptions
- Billing
- SLA
- Support
- Security
- Privacy
- Data Retention
- API Usage
- Incident Response
- Enterprise Plan

## Planned Future Phases

The following are planned and are NOT implemented yet:

- GraphRAG with Neo4j
- Hybrid GraphRAG with Qdrant + Neo4j
- MCP server integration
- MCP client integration
- Enterprise tools and external integrations

## Project Goal

The long-term goal is to evolve the standalone RAG system into an MCP-based enterprise knowledge agent.
