import json
import os
import requests

from env_variables_setup import get_servicenow_auth


def main():
    url = "https://dev385105.service-now.com/api/now/table/change_request"  #service-now instance URL for change_request table API endpoint
    params = {"sysparm_limit": 5}
    auth = get_servicenow_auth()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(url, params=params, auth=auth, headers=headers)
        response.raise_for_status()
        data = response.json()

        results = data.get("result", [])
        if not results:
            print("No results returned from ServiceNow.")
            return

        risk_label_map = {
            "3": "High",
            "2": "Medium",
            "1": "Low",
            "0": "Low",
        }

        mapped_records = []
        for record in results:
            raw_risk = record.get("risk")
            raw_risk_str = str(raw_risk).strip() if raw_risk is not None else ""
            risk_label = risk_label_map.get(raw_risk_str, "Unknown / Not Evaluated")
            mapped_records.append({
                "number": record.get("number"),
                "sys_id": record.get("sys_id"),
                "short_description": record.get("short_description"),
                "state": record.get("state"),
                "risk": risk_label,
            })

        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "pdi_servicenow_changes.json")
        with open(output_path, "w", encoding="utf-8") as output_file:
            json.dump(mapped_records, output_file, indent=2)

        print(f"Saved {len(mapped_records)} records to {output_path}")

    except requests.exceptions.RequestException as err:
        print(f"HTTP request failed: {err}")


if __name__ == "__main__":
    main()
