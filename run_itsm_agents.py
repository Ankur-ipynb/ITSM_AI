'''
### VERSION V1 TO IDENTIFY AGENT GAPS ###
'''
import json
import os

# Disable external OpenTelemetry hooks (keep local LLM validation intact)
os.environ["OTEL_SDK_DISABLED"] = "true"
# Disable CrewAI telemetry and route OpenAI-compatible clients to local Ollama
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OLLAMA_HOST"] = "http://localhost:11434"
# Disable CrewAI tracing and ensure stdout uses UTF-8
os.environ["CREWAI_TRACING_ENABLED"] = "false"
os.environ["CREWAI_DISABLE_TRACING"] = "true"
os.environ["PYTHONIOENCODING"] = "utf-8"

from crewai import Agent, Task, Crew
from crewai.llms.providers.openai_compatible import OpenAICompatibleCompletion


def load_mock_servicenow_data(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_itsm_agent(llm):
    return Agent(
        role="ITSM Change Analyst",
        goal="Assess change request risk and produce a concise Change Advisory Board summary report.",
        backstory=(
            "An expert in analyzing corporate IT infrastructure changes, network routing, "
            "and operating system patches to ensure zero downtime."
        ),
        llm=llm,
        verbose=True,
    )


def build_cab_task(change_requests, agent):
    return Task(
        description=(
            "Read each change request in the provided JSON data, evaluate the risk description, "
            "and generate a brief, professional markdown Change Advisory Board (CAB) summary report. "
            "For each change request, include the number, short_description, state, and risk, "
            "and provide a concise risk evaluation and recommendation in markdown format.\n\n"
            "Raw JSON data:\n"
            f"{json.dumps(change_requests, indent=2)}"
        ),
        expected_output=(
            "A concise markdown CAB summary report that covers each change request, its risk, "
            "and provides a recommendation for the Change Advisory Board."
        ),
        agent=agent,
    )


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "mock_servicenow_changes.json")

    change_requests = load_mock_servicenow_data(json_path)

    # Local Ollama LLM configuration
    llm = OpenAICompatibleCompletion(
        provider="ollama",
        model="llama3.2:1b",
        base_url="http://localhost:11434/v1",
        timeout=60,
        max_retries=3,
    )

    itsm_agent = build_itsm_agent(llm)
    cab_task = build_cab_task(change_requests, itsm_agent)

    # Crew configuration using local Ollama for manager/chat operations
    crew = Crew(
        agents=[itsm_agent],
        tasks=[cab_task],
        manager_llm=llm,
        chat_llm=llm,
        # Ensure function-calling is routed to local Ollama (string accepted)
        function_calling_llm="ollama",
        # Disable internal tracing to avoid external trace uploads
        tracing=False,
        planning=False,
        verbose=True,
    )

    try:
        result = crew.kickoff()
        print("\n=== ITSM Risk Assessment Result ===")
        print(result)
    except Exception as error:
        print("Error running the ITSM Crew:", error)
        print("Confirm that the Ollama server is running at http://localhost:11434 and the model name is correct.")


if __name__ == "__main__":
    main()
