
from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph,END
from app.agents.state import OrbitalOpsState
from app.core.constants import CONFIDENCE_THRESHOLD 
from app.agents.anomaly_detection_agent import make_anomaly_detection_node, TelemetryHistory
from app.agents.research_agent import research_node
from app.agents.root_cause_agent import root_cause_analysis_node
from app.agents.recommendation_agent import recommendation_node
from app.agents.summary_agent import summary_node
from app.agents.human_review_agent import human_review_node
from app.agents.alerting_agent import alerting_node


def telemetry_monitoring_node(state:OrbitalOpsState) -> OrbitalOpsState:
    return state


# def anomaly_detection_node(state:OrbitalOpsState) -> OrbitalOpsState:
#     return state 

# def root_cause_analysis_node(state:OrbitalOpsState) -> OrbitalOpsState:
#     return state

# def research_node(state:OrbitalOpsState) -> OrbitalOpsState:
#     return state

# def recommendation_node(state:OrbitalOpsState) -> OrbitalOpsState:
#     return state

# def human_review_node(state:OrbitalOpsState) -> OrbitalOpsState:
#     return state

# def alerting_node(state:OrbitalOpsState) -> OrbitalOpsState:
#     return state

# def summary_node(state:OrbitalOpsState) -> OrbitalOpsState:
#     return state


def route_after_rca(state:OrbitalOpsState) -> str:
    if state.root_cause_analysis.overall_confidence < CONFIDENCE_THRESHOLD:
        return "low_confidence"
    return "confident"


def route_after_recommendation(state:OrbitalOpsState) -> str:
    if state.recommendation.is_critical:
        return "critical"
    return "not_critical"

def route_after_human_review(state: OrbitalOpsState) -> str:
    if state.human_review.decision == "rejected":
        return "rejected"
    return "approved"


def build_orbitalops_graph(history: TelemetryHistory):
    graph = StateGraph(OrbitalOpsState)

    graph.add_node("telemetry_monitoring",telemetry_monitoring_node)
    graph.add_node("anomaly_detection",make_anomaly_detection_node(history))
    graph.add_node("root_cause_analysis",root_cause_analysis_node)
    graph.add_node("research",research_node)
    graph.add_node("recommendation",recommendation_node)
    graph.add_node("human_review",human_review_node)
    graph.add_node("alerting",alerting_node)
    graph.add_node("summary",summary_node)


    graph.set_entry_point("telemetry_monitoring")

    graph.add_edge("telemetry_monitoring","anomaly_detection")
    #graph.add_edge("anomaly_detection","root_cause_analysis")
    graph.add_edge("anomaly_detection", "research")
    graph.add_edge("research", "root_cause_analysis")

    graph.add_conditional_edges(
        "root_cause_analysis",
        route_after_rca,
        {
            "low_confidence":"human_review",
             "confident": "recommendation",
        }
    )

    graph.add_conditional_edges(
            "recommendation",
            route_after_recommendation,
            {
                "critical":"human_review",
                "not_critical":"alerting"
            }
        )

    graph.add_conditional_edges(
        "human_review",
        route_after_human_review,
        {
            "approved": "alerting",
            "rejected": "summary",
        },
    )
    graph.add_edge("alerting","summary")
    graph.add_edge("summary",END)

    return graph.compile()


if __name__ == "__main__":
    history = TelemetryHistory()
    graph = build_orbitalops_graph(history)
    #print(graph.get_graph().draw_mermaid())
    image_data = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(image_data)
    print("Graph successfully saved to graph.png")






