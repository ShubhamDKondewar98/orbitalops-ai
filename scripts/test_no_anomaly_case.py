# from app.telemetry.simulator import TelemetrySimulator
# from app.agents.anomaly_detection_agent import TelemetryHistory, anomaly_detection_node
# from app.agents.state import OrbitalOpsState
# from datetime import datetime, timezone
# import uuid

# sim = TelemetrySimulator()
# history = TelemetryHistory()


# sim.trigger_scenario("thermal_cascade", duration_ticks=3)

# #for i in range(3):

# reading = sim.generate_reading()

# state = OrbitalOpsState(
#     telemetry=reading,
#     run_id=str(uuid.uuid4()),
#     started_at=datetime.now(timezone.utc),
# )

# result = anomaly_detection_node(state, history)
# print("is_anomaly:", result.anomaly_info.is_anomaly)
# print("detection_method:", result.anomaly_info.detection_method)




###################

from app.telemetry.simulator import TelemetrySimulator

sim = TelemetrySimulator()

sim.trigger_scenario("thermal_cascade", duration_ticks=3)

print("Right after trigger_scenario, BEFORE any generate_reading() call:")
print("active_scenario:", sim.active_scenario)
print("scenario_ticks_remaining:", sim.scenario_ticks_remaining)

print("\nCalling generate_reading() ONE time...")
sim.generate_reading()
print("active_scenario:", sim.active_scenario)
print("scenario_ticks_remaining:", sim.scenario_ticks_remaining)

print("\nCalling generate_reading() a SECOND time...")
sim.generate_reading()
print("active_scenario:", sim.active_scenario)
print("scenario_ticks_remaining:", sim.scenario_ticks_remaining)

print("\nCalling generate_reading() a THIRD time...")
sim.generate_reading()
print("active_scenario:", sim.active_scenario)
print("scenario_ticks_remaining:", sim.scenario_ticks_remaining)

print("\nCalling generate_reading() a FOURTH time...")
sim.generate_reading()
print("active_scenario:", sim.active_scenario)
print("scenario_ticks_remaining:", sim.scenario_ticks_remaining)
