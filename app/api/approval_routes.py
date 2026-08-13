


from fastapi import APIRouter
from pydantic import BaseModel
from app.db.database import get_checkpointer
from app.agents.anomaly_detection_agent import TelemetryHistory
from app.agents.graph import build_orbitalops_graph
from langgraph.types import Command

router = APIRouter()


class ApprovalRequest(BaseModel):
    decision: str


@router.post("/approve/{run_id}")
def approve_run(run_id:str , request: ApprovalRequest):
    history = TelemetryHistory()

    with get_checkpointer() as checkpointer:
        graph = build_orbitalops_graph(history, checkpointer=checkpointer)
        config = {"configurable": {"thread_id": run_id}}

        result = graph.invoke(Command(resume=request.decision), config=config)

        return {
            "run_id": run_id,
            "pipeline_status": result["pipeline_status"],
            "decision": result["human_review"].decision,
        } 


@router.get("/pending/{run_id}")
def get_pending_details(run_id: str):
    history = TelemetryHistory()

    with get_checkpointer() as checkpointer:
        graph = build_orbitalops_graph(history,checkpointer=checkpointer)
        config = {"configurable": {"thread_id": run_id}}

        state = graph.get_state(config)

        if state.interrupts:
            return state.interrupts[0].value
        return {"error": "No pending interrupt found for this run"}











