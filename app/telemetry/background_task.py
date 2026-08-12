import asyncio
from dotenv import load_dotenv
load_dotenv()
from app.telemetry.simulator import TelemetrySimulator
from app.agents.anomaly_detection_agent import TelemetryHistory,anomaly_detection_node
from app.agents.graph import build_orbitalops_graph
from app.agents.state import OrbitalOpsState
from app.db.crud import save_telemetry_reading
from app.core.logging_config import get_logger
from datetime import datetime,timezone
import uuid
logger = get_logger(__name__)


TICK_INTERVAL_SECONDS = 5
COOLDOWN_TICKS = 12


async def run_telemetry_loop(max_ticks: int | None = None, force_scenario: str | None = None):
    sim = TelemetrySimulator()
    history = TelemetryHistory()
    graph = build_orbitalops_graph(history)

    if force_scenario:
        sim.trigger_scenario(force_scenario, duration_ticks=10)

    cooldown_remaining = 0
    tick_count = 0

    while True:

        if max_ticks is not None and tick_count >= max_ticks:
            logger.info(f"Reached max_ticks={max_ticks}, stopping test run")
            break

        reading = sim.generate_reading()
        save_telemetry_reading(reading)

        if cooldown_remaining > 0 :
            cooldown_remaining -= 1

        else:
            state = OrbitalOpsState(
                telemetry=reading,
                run_id=str(uuid.uuid4()),
                started_at=datetime.now(timezone.utc)
            )
            state = anomaly_detection_node(state,history)

            if state.anomaly_info.is_anomaly:
                logger.info(f"Anomaly detected, triggered full pipeline: {state.anomaly_info.anomalous_parameters}")
                graph.invoke(state)
                cooldown_remaining = COOLDOWN_TICKS

        tick_count += 1
        await asyncio.sleep(TICK_INTERVAL_SECONDS)


if __name__ == "__main__":
    logger.info("Starting telemetry background loop")
    asyncio.run(run_telemetry_loop(max_ticks=15, force_scenario="thermal_cascade"))
    #asyncio.run(run_telemetry_loop(max_ticks=15))


    