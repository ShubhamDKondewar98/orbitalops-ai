
from app.core.constants import TELEMETRY_THRESHOLDS, CORRELATED_PARAMETERS,TREND_WINDOW_SIZE, TREND_RATE_THRESHOLDS
from app.agents.state import OrbitalOpsState, AnomalyInfo
from collections import deque 




class TelemetryHistory:
    def __init__(self):
        self.history: dict[str,deque[float]] = {
            param: deque(maxlen=TREND_WINDOW_SIZE)
            for param in TELEMETRY_THRESHOLDS.keys()
        }

    def add_reading(self,telemetry_dict: dict[str,float]) -> None:
        for param, value in telemetry_dict.items():
            if param in self.history:
                self.history[param].append(value)

    def get_window(self,param:str) -> list[float]:
        return list(self.history[param])


def _is_in_any_range(value: float, ranges: list[tuple[float, float]]) -> bool:
    #print("inside _is_in_any_range method")
    for range_min, range_max in ranges:
        if range_min <= value <= range_max:
            return True
    return False


def _classify_parameter(param_name: str, value: float) -> str:
    thresholds = TELEMETRY_THRESHOLDS[param_name]
    
    if _is_in_any_range(value, thresholds["critical_ranges"]):
        return "CRITICAL"
    if _is_in_any_range(value, thresholds["warning_ranges"]):
        return "WARNING"
    return "INFO"

def _calculate_slope(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    total_change = values[-1] - values[0]
    num_steps = len(values) -1

    return total_change / num_steps 

def _is_trending(param_name:str , values : list[float]) -> bool :
    slope = _calculate_slope(values)
    threshold = TREND_RATE_THRESHOLDS[param_name]
    return abs(slope) > threshold 


def anomaly_detection_node(state: OrbitalOpsState, history: TelemetryHistory) -> OrbitalOpsState:
    telemetry = state.telemetry
    telemetry_dict = telemetry.model_dump(exclude={"timestamp"})

    # update rolling history with  new reading
    history.add_reading(telemetry_dict)

    anomalous_parameters: list[str] = []
    correlated_checked: set[str] = set()
    highest_severity = "INFO"
    used_threshold = False
    used_trend = False

    severity_rank = {"INFO": 0, "WARNING": 1, "CRITICAL": 2}

    for param_name, value in telemetry_dict.items():
        threshold_severity = _classify_parameter(param_name, value)
        window = history.get_window(param_name)
        trending = _is_trending(param_name, window)

        is_anomalous_here = threshold_severity != "INFO" or trending

        #print(f"{param_name}: value={value:.2f}, threshold={threshold_severity}, trending={trending}, anomalous={is_anomalous_here}")


        if threshold_severity != "INFO":
            used_threshold = True
        if trending:
            used_trend = True

        if is_anomalous_here:
            anomalous_parameters.append(param_name)
            for correlated_param in CORRELATED_PARAMETERS.get(param_name, []):
                correlated_checked.add(correlated_param)

        if severity_rank[threshold_severity] > severity_rank[highest_severity]:
            highest_severity = threshold_severity

    if used_threshold and used_trend:
        detection_method = "both"
    elif used_trend:
        detection_method = "trend"
    elif used_threshold:
        detection_method = "threshold"
    else:
        detection_method = "none" 

    print(f"--- FINAL: is_anomaly={len(anomalous_parameters) > 0}, severity={highest_severity}, method={detection_method} ---")


    state.anomaly_info = AnomalyInfo(
        is_anomaly=len(anomalous_parameters) > 0,
        severity=highest_severity,
        anomalous_parameters=anomalous_parameters,
        correlated_parameters_checked=list(correlated_checked),
        detection_method=detection_method,
    )

    return state

def make_anomaly_detection_node(history: TelemetryHistory):
    def node(state: OrbitalOpsState) -> OrbitalOpsState:
        return anomaly_detection_node(state, history)
    return node




    








