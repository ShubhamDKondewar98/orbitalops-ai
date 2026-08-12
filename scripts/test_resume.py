from dotenv import load_dotenv
load_dotenv()

from app.db.database import get_checkpointer
from app.agents.anomaly_detection_agent import TelemetryHistory
from app.agents.graph import build_orbitalops_graph
from langgraph.types import Command

RUN_ID = "86f4fe56-a730-420c-a2b1-90b8898d3a91"

history = TelemetryHistory()

with get_checkpointer() as checkpointer:
    graph = build_orbitalops_graph(history, checkpointer=checkpointer)
    config = {"configurable": {"thread_id": RUN_ID}}

    result = graph.invoke(Command(resume="approve"), config=config)

    print("\n=== GRAPH RESUMED AND COMPLETED ===")
    print("Pipeline status:", result["pipeline_status"])
    print("Human decision:", result["human_review"].decision)
