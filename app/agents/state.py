
from pydantic import BaseModel,Field
from datetime import datetime 
from typing import Literal


 
class TelemetryReading(BaseModel):
    timestamp: datetime
    battery_temperature: float
    battery_charge_level: float
    solar_panel_output: float
    fuel_pressure: float
    signal_strength: float
    data_transmission_rate: float
    onboard_cpu_temperature: float
    altitude: float
    velocity: float
    attitude_stability: float


class AnomalyInfo(BaseModel):
    is_anomaly: bool
    severity: Literal["INFO", "WARNING", "CRITICAL"]
    anomalous_parameters: list[str]      #    which parameter trigger this 
    correlated_parameters_checked: list[str]   ##  which parameter need to be checked with anomaly parameter 
    detection_method: Literal["threshold", "trend", "both"]

class PossibleCause(BaseModel):
    cause: str
    confidence: float # 0 to 1
    supporting_evidence: str #   which incident backs this 

class RootCauseAnalysis(BaseModel):
    possible_causes: list[PossibleCause]
    correlated_parameters: list[str]
    requires_human_review: bool
    overall_confidence: float  

class RetrievedDocument(BaseModel):
    source_file: str              # e.g. "IR-001 , 002   etc "
    document_type: Literal["incident_report", "operational_procedure", "mission_knowledge"]
    content_snippet: str          # retrieved chunk
    similarity_score: float       #   how relevant chunk is it

class ResearchFindings(BaseModel):
    retrieved_documents: list[RetrievedDocument]
    query_used: str               # what the agent actually searched for
    total_documents_found: int 

class RecommendedAction(BaseModel):
    action: str
    priority: Literal["LOW", "MEDIUM", "HIGH", "IMMEDIATE"]
    source_reference: str          # which OPS procedure this came from

class Recommendation(BaseModel):
    actions: list[RecommendedAction]
    is_critical: bool              #  helps for hitl triggering 
    grounded_in: list[str]         # which source documents backed these actions

class HumanReviewStatus(BaseModel):
    review_required: bool
    review_reason: Literal["critical_action", "low_rca_confidence", "not_required"]
    decision: Literal["approved", "rejected", "modified", "pending"] | None = None
    modified_action: str | None = None
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    
class OrbitalOpsState(BaseModel):
    # Input
    telemetry: TelemetryReading

    # Agent outputs, filled in progressively as pipeline runs
    anomaly_info: AnomalyInfo | None = None
    root_cause_analysis: RootCauseAnalysis | None = None
    research_findings: ResearchFindings | None = None
    recommendation: Recommendation | None = None
    human_review: HumanReviewStatus | None = None

    # Pipeline health / meta tracking
    pipeline_status: Literal["running", "completed", "degraded", "failed"] = "running"
    failed_stages: list[str] = Field(default_factory=list)
    retry_counts: dict[str, int] = Field(default_factory=dict)
    
    # Feedback (filled in AFTER pipeline completes, by engineer)
    feedback: Literal["useful", "not_useful", "partially_useful"] | None = None

    # Run metadata
    run_id: str
    started_at: datetime
    completed_at: datetime | None = None 



