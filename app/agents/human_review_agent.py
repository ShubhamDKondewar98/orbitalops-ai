from datetime import datetime,timezone
from app.agents.state import OrbitalOpsState,HumanReviewStatus


def human_review_node(state: OrbitalOpsState) -> OrbitalOpsState:
    if state.root_cause_analysis.overall_confidence < 0.5:
        reason = "low_rca_confidence"

    else:
        reason = "critical_action"

    print(f"\n=== HUMAN REVIEW REQUIRED ===")
    print(f"Reason: {reason}")
    print(f"Severity: {state.anomaly_info.severity}")
    print(f"Anomalous parameters: {', '.join(state.anomaly_info.anomalous_parameters)}")

    # print(f"\nTop root cause: {state.root_cause_analysis.possible_causes[0].cause}")
    # print(f"RCA confidence: {state.root_cause_analysis.overall_confidence}")

    if state.root_cause_analysis.possible_causes:
        print(f"\nTop root cause: {state.root_cause_analysis.possible_causes[0].cause}")
    else:
        print("\nTop root cause: No cause identified (RCA failed to produce results)")

    print(f"RCA confidence: {state.root_cause_analysis.overall_confidence}")

    if state.recommendation:
        print("\nRecommended actions")
        for action in state.recommendation.actions:
            print(f" [{action.priority}]  {action.action}")

    else:
        print("\n No recommendation available - confidence too low to generate one.")


    decision_input =input("\n Approve this? (approve/reject): ").strip().lower()
    decision = "approved" if decision_input == "approve" else "rejected"

    state.human_review = HumanReviewStatus(
        review_required=True,
        review_reason=reason,
        decision=decision,
        reviewed_by="test engineer",
        reviewed_at=datetime.now(timezone.utc),
    )

    return state


    
