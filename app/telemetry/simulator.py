
import random 
from datetime import datetime,timezone
from app.agents.state import TelemetryReading


#  safe midpoints when nothing to worry 
NOMINAL_BASELINES = {
    "battery_temperature": 25.0,
    "battery_charge_level": 78.0,
    "solar_panel_output": 200.0,
    "fuel_pressure": 250.0,
    "signal_strength": -70.0,
    "data_transmission_rate": 120.0,
    "onboard_cpu_temperature": 35.0,
    "altitude": 530.0,
    "velocity": 7.70,
    "attitude_stability": 0.3
}

DRIFT_MAGNITUDES = {
    "battery_temperature": 0.3,
    "battery_charge_level": 0.4,
    "solar_panel_output": 1.0,
    "fuel_pressure": 1.5,
    "signal_strength": 0.5,
    "data_transmission_rate": 2.0,
    "onboard_cpu_temperature": 0.3,
    "altitude": 0.2,
    "velocity": 0.01,
    "attitude_stability": 0.02,
}


##  differnet scenario 

ANOMALY_SCENARIOS = {
    "thermal_cascade": {
        "battery_temperature": 78.0,
        "attitude_stability": 3.5,
        "onboard_cpu_temperature": 58.0,
    },

    "communication_degradation": {
        "attitude_stability": 3.8,
        "signal_strength": -102.0,
        "data_transmission_rate": 18.0,
    } ,

    "power_budget_stress": {
        "solar_panel_output": 158.0,
        "battery_charge_level": 45.0,
    } ,

    "propulsion_degradation": {
        "fuel_pressure": 188.0,
    } ,
}



class TelemetrySimulator:
    def __init__(self):
        self.current_values = NOMINAL_BASELINES.copy()
        self.active_scenario: str | None = None
        self.scenario_ticks_remaining: int = 0

    def trigger_scenario(self, scenario_name: str, duration_ticks: int = 10) -> None:
        if scenario_name not in ANOMALY_SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        self.active_scenario = scenario_name
        self.scenario_ticks_remaining = duration_ticks

    # def _apply_drift(self) -> None:
    #     for param in self.current_values:
    #         drift = random.uniform(-0.3, 0.3)
    #         self.current_values[param] += drift

    def _apply_drift(self) -> None:
        for param in self.current_values:
            magnitude = DRIFT_MAGNITUDES[param]
            drift = random.uniform(-magnitude, magnitude)
            self.current_values[param] += drift

    # def _apply_scenario_pull(self) -> None:
    #     targets = ANOMALY_SCENARIOS[self.active_scenario]
    #     for param, target_value in targets.items():
    #         current = self.current_values[param]
    #         # move ~25% of the way toward target each tick, plus small noise
    #         step = (target_value - current) * 0.25
    #         self.current_values[param] = current + step + random.uniform(-0.5, 0.5)

    def _apply_scenario_pull(self) -> None:
        targets = ANOMALY_SCENARIOS[self.active_scenario]
        for param, target_value in targets.items():
            current = self.current_values[param]
            step = (target_value - current) * 0.25
            magnitude = DRIFT_MAGNITUDES[param]
            self.current_values[param] = current + step + random.uniform(-magnitude, magnitude) 

    def _recover_toward_baseline(self) -> None:
        for param, baseline in NOMINAL_BASELINES.items():
            current = self.current_values[param]
            step = (baseline - current) * 0.1
            self.current_values[param] = current + step

    def generate_reading(self) -> TelemetryReading:
        self._apply_drift()

        if self.active_scenario:
            self._apply_scenario_pull()
            self.scenario_ticks_remaining -= 1
            if self.scenario_ticks_remaining <= 0:
                self.active_scenario = None
        else:
            self._recover_toward_baseline()
            # small chance of a random background anomaly
            if random.random() < 0.02:
                self.trigger_scenario(random.choice(list(ANOMALY_SCENARIOS.keys())))

        return TelemetryReading(
            timestamp=datetime.now(timezone.utc),
            **self.current_values,
        )
     

        