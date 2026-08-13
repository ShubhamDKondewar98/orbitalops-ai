
import streamlit as st
import requests
import plotly.express as px

API_URL = "http://localhost:8000"

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



