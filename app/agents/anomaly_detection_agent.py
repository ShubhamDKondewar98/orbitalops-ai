
from app.core.constants import TELEMETRY_THRESHOLDS, CORRELATED_PARAMETERS
from app.agents.state import OrbitalOpsState, AnomalyInfo


def _is_in_any_range(value: float, ranges: list[tuple[float, float]]) -> bool:
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


def anomaly_detection_node(state: OrbitalOpsState) -> OrbitalOpsState:
    telemetry = state.telemetry
    telemetry_dict = telemetry.model_dump(exclude={"timestamp"})

    anomalous_parameters: list[str] = []
    correlated_checked: set[str] = set()
    highest_severity = "INFO"

    severity_rank = {"INFO": 0, "WARNING": 1, "CRITICAL": 2}

    for param_name, value in telemetry_dict.items():
        severity = _classify_parameter(param_name, value)

        if severity != "INFO":
            anomalous_parameters.append(param_name)

            # check correlated parameters too, per OPS-MANUAL-001 Section 2.2
            for correlated_param in CORRELATED_PARAMETERS.get(param_name, []):  
                #  .get(param_name, []) if key is ot presne tit will return empt dict instead of failing 
                correlated_checked.add(correlated_param)

        if severity_rank[severity] > severity_rank[highest_severity]:
            highest_severity = severity

    state.anomaly_info = AnomalyInfo(
        is_anomaly=len(anomalous_parameters) > 0,
        severity=highest_severity,
        anomalous_parameters=anomalous_parameters,
        correlated_parameters_checked=list(correlated_checked),
        detection_method="threshold",
    )

    return state