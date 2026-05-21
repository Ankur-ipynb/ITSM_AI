# ITSM AI Edge Agent

**Fully local, privacy-first AI agent for ServiceNow ITSM Change Management.**

An end-to-end offline system that extracts Change Requests from ServiceNow, processes them with PySpark, and generates professional Change Advisory Board (CAB) risk assessments using a local Ollama LLM + CrewAI.

---

## ✨ Features

- **100% Local & Private** — Runs entirely on your machine (no data leaves your laptop)
- **Live ServiceNow Integration** — Pulls real Change Requests from your PDI
- **Enterprise-grade Processing** — PySpark data cleaning & transformation
- **Structured AI Output** — Pydantic-validated CAB reports
- **Production Orchestrator** — One-command pipeline with logging
- **Zero Cost** — Uses free local models (Ollama)

---

## Architecture

```mermaid
flowchart LR
    A[ServiceNow PDI] --> B[fetch_sn_data.py]
    B --> C[PySpark Processing]
    C --> D[run_itsm_agents.py]
    D --> E[CAB Risk Report]
    F[Ollama LLM] <--> D
