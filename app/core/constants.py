


CONFIDENCE_THRESHOLD = 0.5

TELEMETRY_THRESHOLDS = {
    "battery_temperature": {
    "nominal": (10, 45),
    "warning_ranges": [(45, 60), (0, 5)],
    "critical_ranges": [(60, 200), (-100, 0)],
    }, 
    "battery_charge_level": {
        "nominal": (60, 95),
        "warning_ranges": [(40, 60), (97, 99)],
        "critical_ranges": [(0, 40), (99, 100)],
    },
    "solar_panel_output": {
        "nominal": (180, 220),
        "warning_ranges": [(150, 180)],
        "critical_ranges": [(0, 150)],
    },
    "fuel_pressure": {
        "nominal": (220, 280),
        "warning_ranges": [(190, 220)],
        "critical_ranges": [(0, 190)],
    },
    "signal_strength": {
        "nominal": (-90, -60),
        "warning_ranges": [(-100, -90)],
        "critical_ranges": [(-200, -100)],
    },
    "data_transmission_rate": {
        "nominal": (50, 200),
        "warning_ranges": [(20, 50)],
        "critical_ranges": [(0, 20)],
    },
    "onboard_cpu_temperature": {
        "nominal": (20, 60),
        "warning_ranges": [(60, 70)],
        "critical_ranges": [(70, 200)],
    },
    "altitude": {
        "nominal": (520, 540),
        "warning_ranges": [(510, 520), (540, 550)],
        "critical_ranges": [(0, 510), (550, 1000)],
    },
    "velocity": {
        "nominal": (7.60, 7.80),
        "warning_ranges": [(7.50, 7.60), (7.80, 7.90)],
        "critical_ranges": [(0, 7.50), (7.90, 20.0)],
    },
    "attitude_stability": {
        "nominal": (0, 1.0),
        "warning_ranges": [(1.0, 3.0)],
        "critical_ranges": [(3.0, 180.0)],
    },
}


CORRELATED_PARAMETERS = {
    "battery_temperature": ["attitude_stability", "solar_panel_output"],
    "onboard_cpu_temperature": ["attitude_stability"],
    "signal_strength": ["attitude_stability"],
    "battery_charge_level": ["solar_panel_output"],
    "fuel_pressure": ["velocity"],
    "attitude_stability": ["battery_temperature", "onboard_cpu_temperature", "signal_strength"],
    "solar_panel_output": ["battery_temperature", "battery_charge_level"],
    "velocity": ["fuel_pressure"],
    "data_transmission_rate": ["signal_strength"],
    "altitude": [],
}