from app.telemetry.simulator import TelemetrySimulator

sim = TelemetrySimulator()

print("=== IDLE - just drift, no scenario ===")
for i in range(3):
    reading = sim.generate_reading()
    print(f"Tick {i}: battery_temp={reading.battery_temperature:.2f}, fuel_pressure={reading.fuel_pressure:.2f}")

print("\n=== TRIGGERING thermal_cascade ===")
sim.trigger_scenario("thermal_cascade", duration_ticks=5)
for i in range(5):
    reading = sim.generate_reading()
    print(f"Tick {i}: battery_temp={reading.battery_temperature:.2f}, attitude={reading.attitude_stability:.2f}, cpu_temp={reading.onboard_cpu_temperature:.2f}")

print("\n=== RECOVERY - scenario should be over now ===")
for i in range(5):
    reading = sim.generate_reading()
    print(f"Tick {i}: battery_temp={reading.battery_temperature:.2f}")
