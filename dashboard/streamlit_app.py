
import streamlit as st
import requests
import plotly.express as px
import os

#API_URL = "http://localhost:8000"

#API_URL = "http://orbitalops-backend:8000"   #   docker  

API_URL = os.getenv("API_URL", "http://localhost:8000")


st.set_page_config(page_title="OrbitalOps AI - Mission Control",layout="wide")
st.title("🛰️ OrbitalOps AI — Mission Control") 


col1,col2 = st.columns(2)

with col1:
    if st.button("▶️ Start Simulation"):
        response = requests.post(f"{API_URL}/simulation/start")
        st.success(response.json())

with col2:
    if st.button("⏹️ Stop Simulation"):
        response = requests.post(f"{API_URL}/simulation/stop")
        st.success(response.json())

st.header("📡 live Telemetry Feed")

if st.button("🔄 Refresh Telemetry"):
    response = requests.get(f"{API_URL}/telemetry/latest")
    reading = response.json()

    if reading:
        import pandas as pd
        df = pd.DataFrame(reading)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")
        df["time_label"] = df["timestamp"].dt.strftime("%H:%M:%S")


        # st.line_chart(df.set_index("time_label")[["battery_temperature", "onboard_cpu_temperature"]])
        
        fig = px.line(
            df,
            x="timestamp",
            y=["battery_temperature", "onboard_cpu_temperature"],
            title="Battery & CPU Temperature Over Time",
            color_discrete_map={
                "battery_temperature": "#FF6B6B",
                "onboard_cpu_temperature": "#4ECDC4",
                },
            )
        fig.update_layout(height=350, yaxis_title="Temperature (°C)")
        st.plotly_chart(fig, use_container_width=True)
        #st.line_chart(df.set_index("time_label")[["attitude_stability"]])
        fig2 = px.line(
            df,
            x="timestamp",
            y=["attitude_stability"],
            title="Attitude Stability Over Time",
            color_discrete_map={
                "attitude_stability": "#FFD93D",
            },
        )
        fig2.update_layout(height=300, yaxis_title="Deviation (degrees)")
        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(df.drop(columns=["time_label"]))

    else:
        st.info("No telemetry data yet. Start the simulation first.")


st.header("🚨 Active Alerts")

response = requests.get(f"{API_URL}/alerts/pending")
pending = response.json()

if pending:
    for run in pending:
        with st.expander(f"⚠️ {run['severity']} — Run {run['run_id'][:8]}... (started {run['started_at']})"):
            details_resp = requests.get(f"{API_URL}/pending/{run['run_id']}")
            details = details_resp.json()

            st.write(f"**Reason:** {details.get('reason')}")
            st.write(f"**Root Cause:** {details.get('top_cause')}")
            st.write(f"**RCA Confidence:** {details.get('rca_confidence')}")
            st.write("**Recommended Actions:**")
            for action in details.get('actions', []):
                st.write(f"- {action}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Approve", key=f"approve_{run['run_id']}"):
                    resp = requests.post(f"{API_URL}/approve/{run['run_id']}", json={"decision": "approve"})
                    st.success(resp.json())
                    st.rerun()
            with col2:
                if st.button("❌ Reject", key=f"reject_{run['run_id']}"):
                    resp = requests.post(f"{API_URL}/approve/{run['run_id']}", json={"decision": "reject"})
                    st.warning(resp.json())
                    st.rerun()

else:
    st.info("No pending approvals right now.")

st.header("📋 Mission Reports")

alerts_resp = requests.get(f"{API_URL}/alerts")
all_runs = alerts_resp.json()


completed_runs = [r for r in all_runs if r["pipeline_status"] == "completed"]


if completed_runs:
    for run in completed_runs[:10]:
        completed_time = run['completed_at'][:19].replace("T", " ") if run['completed_at'] else "N/A"
        label = f"{run['severity']} —  completed {completed_time}"
        with st.expander(label):
            report_resp = requests.get(f"{API_URL}/reports/{run['run_id']}")
            report = report_resp.json()

            rca = report.get("root_cause_analysis")
            rec = report.get("recommendation")
            review = report.get("human_review")

            if rca and rca.get("possible_causes"):
                top_cause = rca["possible_causes"][0]
                st.write(f"**Root Cause:** {top_cause['cause']}")
                st.write(f"**Confidence:** {rca['overall_confidence']}")

            if rec:
                st.write("**Actions Taken:**")
                for action in rec["actions"]:
                    st.write(f"- [{action['priority']}] {action['action']}")

            if review:
                st.write(f"**Human Decision:** {review['decision']} (by {review['reviewed_by']})")
else:
    st.info("No completed mission reports yet.")



st.markdown(
    "[🔍 View detailed agent traces in LangSmith](https://smith.langchain.com/o/24ebadc0-5bed-4a4b-89da-d5e16f4dc31b/projects/p/2a3447fc-e086-44d9-9b86-8445dff2124e?timeModel=%7B%22duration%22%3A%227d%22%7D&runview=traces&tab=0)"
)