
from fastapi import APIRouter
from app.db.database import get_db_session
from app.db.models import TelemetryReadingDB

router = APIRouter()

@router.get("/telemetry/latest")
def get_latest_telemetry(limit: int = 20):
    session = get_db_session()
    try:
        readings = (
            session.query(TelemetryReadingDB)
            .order_by(TelemetryReadingDB.timestamp.desc())
            .limit(limit)
            .all()
        )
        return readings
    finally:
        session.close()