
from app.db.database import get_db_session
from app.db.models import TelemetryReadingDB,PipelineRunDB,AnomalyDetectionDb, RootCauseAnalysisDB,RecommendationDB,HumanReviewDB
from app.core.logging_config import get_logger
logger = get_logger(__name__)

def save_telemetry_reading(reading):
    session = get_db_session()
    try:
        db_reading = TelemetryReadingDB(
            timestamp = reading.timestamp,
            battery_temperature=reading.battery_temperature,
            battery_charge_level=reading.battery_charge_level,
            solar_panel_output=reading.solar_panel_output,
            fuel_pressure=reading.fuel_pressure,
            signal_strength=reading.signal_strength,
            data_transmission_rate=reading.data_transmission_rate,
            onboard_cpu_temperature=reading.onboard_cpu_temperature,
            altitude=reading.altitude,
            velocity=reading.velocity,
            attitude_stability=reading.attitude_stability,   
        )
        session.add(db_reading)
        session.commit()

    except Exception as e:
        session.rollback()
        #print(f"Failed to save telemetry reading: {e}")
        logger.error(f"Failed to save telemetry reading: {e}")

    finally:
        session.close()


def save_pipeline_run(state):
    session = get_db_session()
    try:
        existing_run = session.query(PipelineRunDB).filter(PipelineRunDB.run_id == state.run_id).first()

        if existing_run:
            existing_run.completed_at = state.completed_at
            existing_run.pipeline_status = state.pipeline_status
            existing_run.severity = state.anomaly_info.severity if state.anomaly_info else None
            existing_run.is_anomaly = state.anomaly_info.is_anomaly if state.anomaly_info else None
        else:   
            session.add(PipelineRunDB(
                run_id=state.run_id,
                started_at=state.started_at,
                completed_at=state.completed_at,
                pipeline_status=state.pipeline_status,
                severity=state.anomaly_info.severity if state.anomaly_info else None,
                is_anomaly=state.anomaly_info.is_anomaly if state.anomaly_info else None,
            ))
            
        session.flush()

        if state.anomaly_info:
            existing = session.query(AnomalyDetectionDb).filter(AnomalyDetectionDb.run_id == state.run_id).first()
            if existing:
                existing.severity = state.anomaly_info.severity
                existing.anomalous_parameters = state.anomaly_info.anomalous_parameters
                existing.correlated_parameters_checked = state.anomaly_info.correlated_parameters_checked
                existing.detection_method = state.anomaly_info.detection_method

            else:
                session.add(AnomalyDetectionDb(
                    run_id=state.run_id,
                    severity=state.anomaly_info.severity,
                    anomalous_parameters=state.anomaly_info.anomalous_parameters,
                    correlated_parameters_checked=state.anomaly_info.correlated_parameters_checked,
                    detection_method=state.anomaly_info.detection_method,
                ))

        if state.root_cause_analysis:
            existing = session.query(RootCauseAnalysisDB).filter(RootCauseAnalysisDB.run_id == state.run_id).first()
            if existing:
                existing.overall_confidence = state.root_cause_analysis.overall_confidence
                existing.requires_human_review = state.root_cause_analysis.requires_human_review
                existing.possible_causes = [c.model_dump() for c in state.root_cause_analysis.possible_causes]

            else:
                session.add(RootCauseAnalysisDB(
                    run_id=state.run_id,
                    overall_confidence=state.root_cause_analysis.overall_confidence,
                    requires_human_review=state.root_cause_analysis.requires_human_review,
                    possible_causes=[c.model_dump() for c in state.root_cause_analysis.possible_causes],
                ))

        if state.recommendation:
            existing = session.query(RecommendationDB).filter(RecommendationDB.run_id == state.run_id).first()
            if existing:
                existing.is_critical = state.recommendation.is_critical
                existing.actions = [a.model_dump() for a in state.recommendation.actions]
                existing.grounded_in = state.recommendation.grounded_in

            else:
                session.add(RecommendationDB(
                    run_id=state.run_id,
                    is_critical=state.recommendation.is_critical,
                    actions=[a.model_dump() for a in state.recommendation.actions],
                    grounded_in=state.recommendation.grounded_in,
                ))

        if state.human_review:
            existing = session.query(HumanReviewDB).filter(HumanReviewDB.run_id == state.run_id).first()
            if existing:
                existing.review_reason = state.human_review.review_reason
                existing.decision = state.human_review.decision
                existing.modified_action = state.human_review.modified_action
                existing.reviewed_by = state.human_review.reviewed_by
                existing.reviewed_at = state.human_review.reviewed_at

            else:
                session.add(HumanReviewDB(
                    run_id=state.run_id,
                    review_reason=state.human_review.review_reason,
                    decision=state.human_review.decision,
                    modified_action=state.human_review.modified_action,
                    reviewed_by=state.human_review.reviewed_by,
                    reviewed_at=state.human_review.reviewed_at,
                ))

        session.commit()
        logger.info(f"Pipeline run {state.run_id} saved to database")

    except Exception as e:
        session.rollback()
        logger.error(f"Failed to save pipeline run: {e}")
    finally:
        session.close() 


def has_pending_approval():
    session = get_db_session()
    try:
        pending = session.query(PipelineRunDB).filter(PipelineRunDB.pipeline_status == "running").first()
        return pending is not None
    finally:
        session.close()