from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import OrbitalOpsState
from datetime import datetime, timezone
from app.db.crud import save_pipeline_run


summary_llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)

summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "You write concise mission status reports for AETHER-1 ground control."),
        ("human", "Anomaly severity: {severity}\n"
              "Root cause: {root_cause}\n"
              "Recommended actions: {actions}\n"
              "Human review status: {review_status}\n\n"
              "Write a 3-4 sentence shift summary of this incident."),

])

summary_chain = summary_prompt | summary_llm


def summary_node(state: OrbitalOpsState) -> OrbitalOpsState:
    if state.recommendation:
        actions_text = "; ".join(val.action for val in state.recommendation.actions) 
    else:
        actions_text = "No recommendation generated - root cause confidence was too low"

    if state.human_review:
        review_status = state.human_review.decision
    else:
        review_status = "not required"

    result = summary_chain.invoke({
        "severity": state.anomaly_info.severity,
        "root_cause": state.root_cause_analysis.possible_causes[0].cause if state.root_cause_analysis.possible_causes else "undetermined",
        "actions": actions_text,
        "review_status": review_status,
    })

    state.pipeline_status = "completed"
    state.completed_at = datetime.now(timezone.utc)

    print("\n=== MISSION SUMMARY ===")
    print(result.content)
    print("========================\n")

    save_pipeline_run(state)
    return state