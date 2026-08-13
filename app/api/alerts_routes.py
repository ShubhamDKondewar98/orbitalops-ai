

from fastapi import APIRouter
from app.db.database import get_db_session
from app.db.models import PipelineRunDB

router= APIRouter()

@router.get("/alerts")
def get_recent_alerts(limit: int =20):
    session = get_db_session()
    try:
        runs = (
            session.query(PipelineRunDB)
            .order_by(PipelineRunDB.started_at.desc())
            .limit(limit)
            .all()
        )
        return runs
    finally:
        session.close()



@router.get("/alerts/pending")
def get_pending_approvals():
    session = get_db_session()
    try:
        runs = (
            session.query(PipelineRunDB)
            .filter(PipelineRunDB.pipeline_status=="running")
            .order_by(PipelineRunDB.started_at.desc())
            .all()
        )
        return runs
    finally:
        session.close()
        
    