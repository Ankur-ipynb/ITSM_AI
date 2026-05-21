```markdown
# ITSM AI Edge Agent - Getting Started

## Disclaimer / Intended Audience

**Note:** This playbook serves as a baseline foundational blueprint for setting up local edge agent networks. Enterprise optimization loops, high-throughput PySpark schema fine-tuning, and production guardrails are maintained natively within the secure runtime modules.

This guide documents the setup and implementation of a fully local, privacy-first ITSM AI agent system integrating ServiceNow, PySpark, DuckDB, Ollama, and CrewAI.

---

## Architecture Overview

The solution consists of the following layers:

| Layer                  | Component                        | Purpose |
|------------------------|----------------------------------|-------|
| Data Source            | Live ServiceNow PDI              | Production cloud ITSM environment |
| Security Layer         | Environment variables            | Secure credential handling |
| Ingestion Engine       | Python REST API client           | Automated JSON extraction |
| Compute / Processing   | Local PySpark Session            | Data cleaning and transformation |
| AI Brain               | Ollama (llama3.2:1b or larger)   | Offline local LLM |
| Orchestration          | CrewAI + Pydantic                | Structured multi-agent risk assessment |

---

## Prerequisites

- Python 3.10+
- GitHub Copilot (recommended for development)
- Sufficient RAM (minimum 8GB, 16GB+ recommended)
- ServiceNow Personal Developer Instance (PDI)

---

## Milestone 1: Local AI Setup (Ollama)

1. Download and install Ollama from [ollama.com](https://ollama.com) for your operating system.

2. In a terminal, pull and run the model:
   ```bash
   ollama run llama3.2:1b
   ```
   (Use `llama3` for systems with more resources.)

3. Verify the model responds to a simple prompt, then exit with `/exit`. Keep Ollama running in the background.

4. Open the project in VS Code, activate the Python virtual environment, and install core libraries:
   ```bash
   pip install langchain-community langchain-core langchain-ollama crewai
   ```

5. Test connectivity using a script that connects via `OllamaLLM` (or `ChatOllama`) to `http://localhost:11434`.

---

## Milestone 2: ServiceNow Integration

### Obtain a PDI
1. Sign up at the [ServiceNow Developer Portal](https://developer.servicenow.com).
2. Request a new Personal Developer Instance (latest release recommended).
3. Save the instance URL, admin credentials.

### Data Ingestion
Create `fetch_sn_data.py` to pull change requests via the ServiceNow Table API using Basic Auth and `requests`.

After initial testing, refactor credentials to use environment variables (`.env` file + `python-dotenv`).

**Optional:** Use `mock_servicenow_changes.json` generator for local development before PDI is ready.

---

## Milestone 3: Data Engineering Pipeline

1. Install processing dependencies:
   ```bash
   pip install pyspark duckdb
   ```

2. Implement `read_mock_servicenow_pyspark.py` (or similar) that:
   - Loads JSON into a Spark DataFrame
   - Applies filters (e.g., risk level)
   - Performs schema standardization
   - Outputs cleaned data for downstream agents

Ensure consistent schema between ingestion and processing (e.g., `risk_level`, `state` as human-readable values).

---

## Milestone 4: Live Data Bridging

Update the fetch script to save output as `pdi_servicenow_changes.json` (or `mock_servicenow_changes.json` for compatibility) with standardized keys:
- `number`
- `sys_id`
- `short_description`
- `state` (display value preferred)
- `risk`

Implement mapping for numeric risk/state codes to labels (High/Medium/Low, Approved, etc.) with fallback to "Unknown".

---

## Milestone 5: Agentic Layer (CrewAI + Local Ollama)

Create `run_itsm_agents.py` (or production equivalent) with:

- Local `OllamaLLM` configuration
- Structured output using Pydantic models (`CABTicketSummary`, `CABReportSchema`)
- Risk assessment agent with clear role, goal, and task instructions
- Telemetry disabled via environment variables

**Key Environment Variables (set at top of orchestrator/agent scripts):**
```python
import os
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["PYTHONIOENCODING"] = "utf-8"
```

---

## Production Orchestrator

`run_pipeline.py` executes the full flow sequentially:
1. `fetch_sn_data.py`
2. PySpark processing
3. Agent risk assessment

Features:
- Centralized logging to `pipeline_execution.log`
- Real-time output streaming
- Error handling and early termination on failure
- UTF-8 handling for emoji-safe logging

---

## Final Production Script (`run_itsm_agents_v2.py` or equivalent)

The final agent script includes:
- Pydantic structured output enforcement
- Post-processing validation and sanitization for missing risk fields
- Graceful handling of "Unknown" risk levels
- Clean markdown-formatted CAB report output

---

## Running the Full Pipeline

```bash
python run_pipeline.py
```

Monitor `pipeline_execution.log` for detailed execution trace.

---

## Security & Best Practices

- Never commit credentials or `.env` files
- Use environment variables for all sensitive data
- Run Ollama and processing locally for data privacy
- Validate and sanitize LLM outputs before use in production decisions
- Keep mock data scripts for offline testing

---

## Next Steps & Extensions

- Schema evolution and incremental loading
- Vector store integration (Chroma / FAISS)
- Larger local models (llama3.1:8b, etc.)
- Scheduled execution (cron / Airflow local)
- Advanced evaluation and human-in-the-loop feedback

This foundation enables fully local, auditable, and extensible ITSM AI capabilities on commodity hardware.
```

**Additional Recommendations for the Git Repository:**

1. **Project Structure Suggestion:**
   ```
   itsm-ai-edge/
   ├── src/
   │   ├── fetch_sn_data.py
   │   ├── process_pyspark_data.py
   │   ├── run_itsm_agents.py
   │   ├── run_pipeline.py
   │   └── env_setup.py
   ├── data/
   │   ├── mock_servicenow_changes.json
   │   └── pdi_servicenow_changes.json
   ├── logs/
   ├── .env.example
   ├── requirements.txt
   ├── README.md
   └── getting_started.md   ← This file
   ```
