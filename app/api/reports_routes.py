from fastapi import APIRouter
from app.db.database import get_db_session
from app.db.models import (
    PipelineRunDB,
    AnomalyDetectionDb,
    RootCauseAnalysisDB,
    RecommendationDB,
    HumanReviewDB,
)

router = APIRouter()

@router.get("/reports/{run_id}")
def get_run_report(run_id: str):
    session = get_db_session()  
    try:
        run = session.query(PipelineRunDB).filter(PipelineRunDB.run_id == run_id).first()
        anomaly = session.query(AnomalyDetectionDb).filter(AnomalyDetectionDb.run_id == run_id).first()
        rca = session.query(RootCauseAnalysisDB).filter(RootCauseAnalysisDB.run_id == run_id).first()
        recommendation = session.query(RecommendationDB).filter(RecommendationDB.run_id == run_id).first()
        human_review = session.query(HumanReviewDB).filter(HumanReviewDB.run_id == run_id).first()

        return {
            "run": run,
            "anomaly_detection": anomaly,
            "root_cause_analysis": rca,
            "recommendation": recommendation,
            "human_review": human_review,
        }
    finally:
        session.close()