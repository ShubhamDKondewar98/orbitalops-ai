from dotenv import load_dotenv
load_dotenv()

from app.core.logging_config import setup_logging
setup_logging()

from app.telemetry.simulator import TelemetrySimulator
from app.agents.anomaly_detection_agent import TelemetryHistory, anomaly_detection_node
from app.agents.research_agent import research_node
from app.agents.root_cause_agent import root_cause_analysis_node
from app.agents.recommendation_agent import recommendation_node
from app.agents.state import OrbitalOpsState
from app.db.crud import save_telemetry_reading, save_pipeline_run
from datetime import datetime, timezone
import uuid

sim = TelemetrySimulator()
history = TelemetryHistory()

print("=== Testing save_telemetry_reading ===")
reading = sim.generate_reading()
save_telemetry_reading(reading)
print("Telemetry reading saved")

print("\n=== Building a real pipeline run ===")
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
state = root_cause_analysis_node(state)
state = recommendation_node(state)
state.pipeline_status = "completed"
state.completed_at = datetime.now(timezone.utc)

print("\n=== Testing save_pipeline_run ===")
save_pipeline_run(state)
print("Pipeline run saved")
print("run_id:", state.run_id)
