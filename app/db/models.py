
from sqlalchemy import create_engine, Column,Integer,Float,DateTime,String,Boolean,ForeignKey,JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime,timezone


Base = declarative_base()


class TelemetryReadingDB(Base):
    __tablename__ = "telemetry_readings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    battery_temperature = Column(Float)
    battery_charge_level = Column(Float)
    solar_panel_output = Column(Float)
    fuel_pressure = Column(Float)
    signal_strength = Column(Float)
    data_transmission_rate = Column(Float)
    onboard_cpu_temperature = Column(Float)
    altitude = Column(Float)
    velocity = Column(Float)
    attitude_stability = Column(Float)

class PipelineRunDB(Base):
    __tablename__ = "pipeline_runs"
    run_id = Column(String, primary_key=True)
    started_at = Column(DateTime)
    completed_at = Column(DateTime, nullable=True)
    pipeline_status = Column(String)
    severity = Column(String, nullable=True)
    is_anomaly = Column(Boolean, nullable=True)


class AnomalyDetectionDb(Base):
    __tablename__ = "anomaly_detections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("pipeline_runs.run_id"))
    severity = Column(String)
    anomalous_parameters = Column(JSON)
    correlated_parameters_checked = Column(JSON)
    detection_method = Column(String)

class RootCauseAnalysisDB(Base):
    __tablename__ = "root_cause_analyses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("pipeline_runs.run_id"))
    overall_confidence = Column(Float)
    requires_human_review = Column(Boolean)
    possible_causes = Column(JSON)

class RecommendationDB(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("pipeline_runs.run_id"))
    is_critical = Column(Boolean)
    actions = Column(JSON)
    grounded_in = Column(JSON)

class HumanReviewDB(Base):
    __tablename__ = "human_reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(String, ForeignKey("pipeline_runs.run_id"))
    review_reason = Column(String)
    decision = Column(String, nullable=True)
    modified_action = Column(String, nullable=True)
    reviewed_by = Column(String, nullable=True)
    reviewed_at = Column(DateTime, nullable=True)