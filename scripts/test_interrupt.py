from dotenv import load_dotenv
load_dotenv()

from app.db.database import get_checkpointer
from app.telemetry.simulator import TelemetrySimulator
from app.agents.anomaly_detection_agent import TelemetryHistory
from app.agents.graph import build_orbitalops_graph
from app.agents.state import OrbitalOpsState
from datetime import datetime, timezone
import uuid

sim = TelemetrySimulator()
history = TelemetryHistory()

sim.trigger_scenario("thermal_cascade", duration_ticks=10)
for i in range(10):
    reading = sim.generate_reading()

run_id = str(uuid.uuid4())
state = OrbitalOpsState(
    telemetry=reading,
    run_id=run_id,
    started_at=datetime.now(timezone.utc),
)

with get_checkpointer() as checkpointer:
    graph = build_orbitalops_graph(history, checkpointer=checkpointer)
    config = {"configurable": {"thread_id": run_id}}

    result = graph.invoke(state, config=config)
    print("\n=== GRAPH PAUSED ===")
    print(result)
