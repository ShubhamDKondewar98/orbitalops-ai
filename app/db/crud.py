
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
        db_run = PipelineRunDB(
            run_id=state.run_id,
            started_at=state.started_at,
            completed_at=state.completed_at,
            pipeline_status=state.pipeline_status,
            severity=state.anomaly_info.severity if state.anomaly_info else None,
            is_anomaly=state.anomaly_info.is_anomaly if state.anomaly_info else None,
        )
        session.add(db_run)
        session.flush()

        if state.anomaly_info:
            session.add(AnomalyDetectionDb(
                run_id=state.run_id,
                severity=state.anomaly_info.severity,
                anomalous_parameters=state.anomaly_info.anomalous_parameters,
                correlated_parameters_checked=state.anomaly_info.correlated_parameters_checked,
                detection_method=state.anomaly_info.detection_method,
            ))

        if state.root_cause_analysis:
            session.add(RootCauseAnalysisDB(
                run_id=state.run_id,
                overall_confidence=state.root_cause_analysis.overall_confidence,
                requires_human_review=state.root_cause_analysis.requires_human_review,
                possible_causes=[c.model_dump() for c in state.root_cause_analysis.possible_causes],
            ))

        if state.recommendation:
            session.add(RecommendationDB(
                run_id=state.run_id,
                is_critical=state.recommendation.is_critical,
                actions=[a.model_dump() for a in state.recommendation.actions],
                grounded_in=state.recommendation.grounded_in,
            ))

        if state.human_review:
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
        