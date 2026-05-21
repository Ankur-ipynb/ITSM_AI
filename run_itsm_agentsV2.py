import json
import os
from typing import List, Optional
from pydantic import BaseModel, Field

# Disable external OpenTelemetry hooks and telemetry
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

# Force CrewAI to route standard OpenAI endpoints locally if fallback occurs
os.environ["OPENAI_API_KEY"] = "NA"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"

# Force output to use UTF-8
os.environ["PYTHONIOENCODING"] = "utf-8"

from crewai import Agent, Task, Crew


# 1. Define the strict Pydantic structures with built-in choices for the 1B model
class CABTicketSummary(BaseModel):
    entry_number: int = Field(description="The sequential index number of this item starting at 1.")
    ticket_number: str = Field(description="The ServiceNow change ticket number (e.g., CHG0000024).")
    short_description: str = Field(description="The short description text from the change request.")
    state: str = Field(description="The state value from the ticket.")
    risk_level: Optional[str] = Field(
        description="The risk value straight from the ticket. Write 'Unknown' if empty, blank, or missing."
    )
    risk_assessment: Optional[str] = Field(
        description="A ultra-short 1-sentence evaluation under 15 words explaining the technical impact or downtime risk."
    )
    cab_recommendation: Optional[str] = Field(
        description=(
            "A standard 1-sentence engineering action step under 15 words. "
            "GUIDELINE: If risk is HIGH, recommend executing only during a weekend off-peak maintenance window. "
            "If risk is MEDIUM, recommend peer-reviewing rollback steps before execution. "
            "If risk is LOW, recommend standard operational implementation."
        )
    )


class CABReportSchema(BaseModel):
    items: List[CABTicketSummary] = Field(description="The sequential list of all evaluated change requests.")


def load_mock_servicenow_data(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_itsm_agent(llm_name: str):
    return Agent(
        role="ITSM Change Analyst",
        goal="Extract data from corporate IT infrastructure changes into structured risk profiles.",
        backstory=(
            "An exact operational parser trained to extract metrics into programmatic objects without adding filler text."
        ),
        llm=llm_name,
        verbose=True,  # Keeps the awesome scrolling terminal blocks active for the video!
    )


def build_cab_task(change_requests, agent):
    total_items = len(change_requests)

    return Task(
        description=(
            f"Extract and parse all {total_items} change request items from the provided JSON array. "
            f"You must parse exactly {total_items} objects matching the input sequence order.\n\n"
            "CRITICAL VALUE EXTRACTION RULES:\n"
            "1. Read the risk details provided for each ticket.\n"
            "2. Keep all text arguments strictly concise and under 15 words.\n"
            "3. Provide realistic CAB engineering recommendations based on the ticket's technical risk.\n\n"
            "Raw JSON data to process:\n"
            f"{json.dumps(change_requests, indent=2)}"
        ),
        expected_output=f"A structured Pydantic object containing exactly {total_items} validated ticket records.",
        output_pydantic=CABReportSchema,
        agent=agent,
    )


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "pdi_servicenow_changes.json")

    try:
        change_requests = load_mock_servicenow_data(json_path)
    except FileNotFoundError:
        print(f"Error: Could not find JSON file at {json_path}")
        return

    local_llm = "ollama/llama3.2:1b"

    itsm_agent = build_itsm_agent(local_llm)
    cab_task = build_cab_task(change_requests, itsm_agent)

    crew = Crew(
        agents=[itsm_agent],
        tasks=[cab_task],
        manager_llm=local_llm,
        chat_llm=local_llm,
        function_calling_llm=local_llm,
        max_tokens=4096,
        tracing=False,
        planning=False,
        verbose=True,  # Enabled for visual demo scrolling
    )

    try:
        crew_output = crew.kickoff()
        structured_data = crew_output.pydantic
        
        print("\n\n" + "🚀 " * 20)
        print("💡 AGENT EXECUTION COMPLETE -> GENERATING FINAL PRESENTATION REPORT")
        print("🚀 " * 20 + "\n")
        
        print("=" * 80)
        print("                        FINAL CAB RISK ASSESSMENT REPORT                        ")
        print("=" * 80 + "\n")
        
        tickets = structured_data.items if structured_data else []
        
        for item in tickets:
            risk_lvl = str(getattr(item, "risk_level", "")).strip().lower()
            ticket_num = getattr(item, "ticket_number", "Unknown")
            short_desc = getattr(item, "short_description", "No Description")
            state_val = getattr(item, "state", "Unknown")
            
            is_empty_or_null = not risk_lvl or risk_lvl in ["none", "null", "empty", ""]
            is_unconfirmed = any(x in risk_lvl for x in ["unknown", "not evaluated"])
            
            if is_empty_or_null or is_unconfirmed:
                final_risk_level = "Unknown"
                final_assessment = "No risk evaluation available."
                final_recommendation = "Deferring recommendation until risk assessment fields are completed in ServiceNow."
            else:
                final_risk_level = str(getattr(item, "risk_level")).upper()
                final_assessment = getattr(item, "risk_assessment", "No assessment provided.")
                rec_val = getattr(item, "cab_recommendation", "").strip()
                final_recommendation = rec_val if rec_val else "Follow standard maintenance window protocols."

            print(f"### Entry {getattr(item, 'entry_number', '?')} / {len(change_requests)}: {ticket_num} - {short_desc}")
            print(f"* **State:** {state_val}")
            print(f"* **Risk Level:** {final_risk_level}")
            print(f"* **Risk Assessment:** {final_assessment}")
            print(f"* **CAB Recommendation:** {final_recommendation}\n")
            
        print("=" * 80)

    except Exception as error:
        print("Error running the ITSM Crew:", error)


if __name__ == "__main__":
    main()
