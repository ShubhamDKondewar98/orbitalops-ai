
from dotenv import load_dotenv
load_dotenv()

from app.telemetry.simulator import TelemetrySimulator
from app.agents.anomaly_detection_agent import TelemetryHistory
from app.agents.graph import build_orbitalops_graph
from app.agents.state import OrbitalOpsState
from datetime import datetime,timezone
import uuid


sim = TelemetrySimulator()
history = TelemetryHistory()
graph = build_orbitalops_graph(history)


sim.trigger_scenario("thermal_cascade", duration_ticks=10)

for i in range(10):
    reading = sim.generate_reading()

state = OrbitalOpsState(
    telemetry=reading,
    run_id= str(uuid.uuid4()),
    started_at=datetime.now(timezone.utc),
    
)

result = graph.invoke(state)

print("Pipeline status:" , result["pipeline_status"])