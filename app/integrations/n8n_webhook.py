
import requests
import os
from app.agents.state import OrbitalOpsState


def send_alert(state):
    webhook_url = os.getenv("N8N_WEBHOOK_URL")

    payload = {
        "severity": state.anomaly_info.severity,
        "anomalous_parameters": state.anomaly_info.anomalous_parameters,
        "root_cause": state.root_cause_analysis.possible_causes[0].cause,
        "confidence": state.root_cause_analysis.overall_confidence,
        "actions": [a.action for a in state.recommendation.actions] if state.recommendation else [],
        "human_decision": state.human_review.decision if state.human_review else "not required",
        "run_id": state.run_id,
    }

    response = requests.post(webhook_url, json=payload, timeout=10)
    return response.status_code == 200

