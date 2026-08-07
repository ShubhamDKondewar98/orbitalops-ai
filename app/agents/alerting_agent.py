

from app.integrations.n8n_webhook import send_alert
from app.agents.state import OrbitalOpsState


def alerting_node(state: OrbitalOpsState) -> OrbitalOpsState:
    success = send_alert(state)

    if success:
        print("Alert send successfullu via N8N")
    else:
        print("Alert failed to send ")

    return state
