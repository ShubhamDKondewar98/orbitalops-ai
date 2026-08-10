from dotenv import load_dotenv
load_dotenv()

from app.core.logging_config import setup_logging
setup_logging()

from app.telemetry.simulator import TelemetrySimulator
from app.agents.anomaly_detection_agent import TelemetryHistory, anomaly_detection_node
from app.agents.research_agent import research_node
from app.agents.state import OrbitalOpsState
from datetime import datetime, timezone
import uuid

sim = TelemetrySimulator()
history = TelemetryHistory()
sim.trigger_scenario("thermal_cascade", duration_ticks=10)

for i in range(10):
    reading = sim.generate_reading()

state = OrbitalOpsState(
    telemetry=reading,
    run_id=str(uuid.uuid4()),
    started_at=datetime.now(timezone.utc),
)
state = anomaly_detection_node(state, history)
state = research_node(state)

print("\n--- FINAL CHECK ---")
print("Pipeline status:", state.pipeline_status)
print("Failed stages:", state.failed_stages)
print("Retry counts:", state.retry_counts)
print("Total documents found:", state.research_findings.total_documents_found)
