"""Generate a mock ServiceNow change_request JSON file."""
''' USE BELOW SCRIPT WHEN MISSING SERVICE-NOW PDI TO MOCK '''
import json


def generate_mock_changes():
    data = [
        {
            "number": "CHG0000001",
            "sys_id": "a1b2c3d4e5f678901234567890abcdef",
            "short_description": "Cloud migration for development environment",
            "state": "New",
            "risk": "Low",
            "assignment_group": "Cloud Services"
        },
        {
            "number": "CHG0000002",
            "sys_id": "b2c3d4e5f678901234567890abcdefa1",
            "short_description": "Database server update for compliance",
            "state": "Authorize",
            "risk": "Medium",
            "assignment_group": "Database Team"
        },
        {
            "number": "CHG0000003",
            "sys_id": "c3d4e5f678901234567890abcdefa1b2",
            "short_description": "Azure cloud instance patching",
            "state": "Scheduled",
            "risk": "High",
            "assignment_group": "Infrastructure"
        },
        {
            "number": "CHG0000004",
            "sys_id": "d4e5f678901234567890abcdefa1b2c3",
            "short_description": "Server firmware update for data center",
            "state": "New",
            "risk": "Medium",
            "assignment_group": "Server Operations"
        },
        {
            "number": "CHG0000005",
            "sys_id": "e5f678901234567890abcdefa1b2c3d4",
            "short_description": "Cloud workload migration to new tenant",
            "state": "Authorize",
            "risk": "High",
            "assignment_group": "Cloud Services"
        }
    ]
    return data


def save_mock_changes(filename="pdi_servicenow_changes.json"):
    mock_data = generate_mock_changes()
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(mock_data, json_file, indent=2)
    print(f"Mock ServiceNow change_request JSON saved to {filename}")


if __name__ == "__main__":
    save_mock_changes()
