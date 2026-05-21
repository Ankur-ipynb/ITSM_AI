# Copilot Prompts Used in Development

This document contains the **exact prompts** used with GitHub Copilot Chat during the development of this project, as documented in the original playbook.

---

## 1. Milestone 1: Ollama Connection Test

**Prompt:**
> "Write a simple Python script using langchain_ollama to connect to my local Ollama instance running 'llama3'. The script should send a prompt asking 'What is Change Management in ITSM?' and print out the response from the local model. Include basic error handling in case Ollama isn't running."

---

## 2. Milestone 2: ServiceNow Data Fetch

**Prompt:**
> "Write a Python script using the requests library to fetch the top 5 records from my live ServiceNow instance.
> • Target URL: https://dev385105.service-now.com/api/now/table/change_request
> • Query parameters: limit the results to 5 records.
> • Authentication: Use Basic Authentication with username 'admin' and a password string placeholder.
> • Headers: Set 'Accept' and 'Content-Type' to 'application/json'.
> • Execution: Loop through the JSON response 'result' array. Parse and print out the number, short_description, and sys_id for each change request. Include response.raise_for_status() to cleanly catch any HTTP errors."

---

## 3. Milestone 2-A: Mock Data Generator

**Prompt:**
> "Write a Python script that generates a mock JSON file simulating the raw REST API response from a ServiceNow change_request table.
> The JSON should contain a list of 5 dictionaries. Each dictionary must include standard ITSM fields: number (e.g., CHG0000001), sys_id, short_description (related to cloud migrations or server updates), state (e.g., New, Authorize, Scheduled), risk (High/Medium/Low), and assignment_group.
> The script should automatically save this data as a file named mock_servicenow_changes.json in the current directory."

---

## 4. Milestone 3: PySpark Processing

**Prompt:**
> "Write a local PySpark script that reads the mock ServiceNow JSON data from mock_servicenow_changes.json.
> 1. Initialize a local Spark session.
> 2. Load the JSON file into a Spark DataFrame.
> 3. Filter the DataFrame to find all records where the risk is 'High' or 'Medium'.
> 4. Select only the number, short_description, risk, and assignment_group columns.
> 5. Print the filtered DataFrame to the terminal console using .show().
> Include basic error handling if the file does not exist."

---

## 5. Milestone 4: Live to JSON Bridge

**Prompt:**
> "Modify fetch_sn_data.py so that instead of just printing out the data records to the terminal, it maps the JSON keys to match our standard schema and saves the final full list of 5 records as a JSON file named mock_servicenow_changes.json in the current working directory.
> Map the keys exactly as: number, sys_id, short_description, state, and risk from the raw data object."

---

## 6. Milestone 5: CrewAI Agent (Initial Version)

**Prompt:**
> "Write a Python script using crewai and langchain_ollama to create an automated ITSM Risk Assessment Agent.
> 1. Import Agent, Task, and Crew from crewai. Import OllamaLLM from langchain_ollama.
> 2. Initialize the local LLM using OllamaLLM(model="llama3.2:1b", base_url="http://localhost:11434"). Pass this LLM instance into the CrewAI configuration.
> 3. Read the JSON data from mock_servicenow_changes.json using standard Python json parsing to serve as the context for our task.
> 4. Define an Agent named 'ITSM Change Analyst' with a role of 'Senior Infrastructure Risk Assessor'. Give them a backstory: 'An expert in analyzing corporate IT infrastructure changes, network routing, and operating system patches to ensure zero downtime.'
> 5. Define a Task that takes the raw JSON data and tells the agent to read each change request, evaluate the risk description, and generate a brief, professional markdown Change Advisory Board (CAB) summary report.
> 6. Combine them into a Crew and kick off the process. Print the final result."

---

## 7. Production Orchestrator (`run_pipeline.py`)

**Prompt:**
> "Write a production-grade Python script named run_pipeline.py that orchestrates three files sequentially: fetch_sn_data.py, read_mock_servicenow_pyspark.py, and run_itsm_agents.py.
> 1. Use Python's built-in logging module to log events to both the console and a file named pipeline_execution.log. Format logs with %(asctime)s - %(levelname)s - %(message)s.
> 2. Use subprocess.Popen with stdout=subprocess.PIPE and stderr=subprocess.STDOUT to execute each script.
> 3. Stream the output of each script line-by-line in real-time. Write each line directly into the pipeline_execution.log file using logging.info().
> 4. Check the return code of each process. If a script exits with a non-zero status code, log an error to the file and terminate the remaining pipeline steps immediately."

---

## 8. Final Production Agent Script (V2)

**Prompt:**
> Create a complete Python script using CrewAI, Pydantic, and local Ollama to automate an ITSM Change Advisory Board (CAB) risk report from a ServiceNow JSON file cross-referencing initial version:
> 
> The script must be fully self-contained and implement the following specifications exactly:
> 1. ENVIRONMENT & MODEL ROUTING:
> - Disable telemetry and OpenTelemetry by setting "OTEL_SDK_DISABLED"="true", "CREWAI_DISABLE_TELEMETRY"="true", and "PYTHONIOENCODING"="utf-8" in os.environ.
> - Route standard OpenAI calls locally to Ollama by mapping "OPENAI_API_KEY"="NA" and "OPENAI_API_BASE"="http://localhost:port/v1".
> - Set the local engine string variable to "ollama/llama3.2:1b".
> 
> 2. STRUCTURED PYDANTIC DATA EXTRACTION:
> - Create a Pydantic class named 'CABTicketSummary' inheriting from BaseModel with fields: entry_number (int), ticket_number (str), short_description (str), state (str), risk_level (Optional[str]), risk_assessment (Optional[str]), and cab_recommendation (Optional[str]).
> - Inside the cab_recommendation field description, provide explicit guidelines for the 1B model...
> 
> (Full prompt continues with structured output, validation layer, and visual presentation as per the final milestone)

---

## Additional Fix Prompts

- Telemetry disable prompt
- Character encoding fix for `run_pipeline.py`
- Pydantic ValidationError resolution prompt

---

**Note:** These prompts were used iteratively with GitHub Copilot. Many scripts went through multiple refinement cycles using follow-up prompts for bug fixes (telemetry, schema mapping, encoding issues, etc.).
