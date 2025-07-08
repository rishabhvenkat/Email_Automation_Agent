import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Change if your API runs elsewhere

st.set_page_config(page_title="AI Email Support Dashboard", layout="wide")
st.title("AI Email Support Dashboard")

# Fetch dashboard stats
response = requests.get(f"{API_URL}/dashboard")
data = response.json()
totals = data["totals"]
query_breakdown = data["query_breakdown"]
allowed_domains = data.get("allowed_domains", [])

# Sidebar for config
st.sidebar.header("Configuration")
all_domains = ["Track and Trace", "Vessel Schedule", "Customs", "Invoice", "Other"]
selected_domains = st.sidebar.multiselect(
    "Select domains to auto-reply",
    options=all_domains,
    default=allowed_domains,
)

if st.sidebar.button("Update Automation Domains"):
    res = requests.post(f"{API_URL}/config", json={"allowed_domains": selected_domains})
    if res.status_code == 200:
        st.sidebar.success("Updated configuration!")

# Run now button
if st.sidebar.button("Run Email Processor Now"):
    res = requests.post(f"{API_URL}/process-emails")
    if res.status_code == 200:
        st.sidebar.success("Email processing started!")
    else:
        st.sidebar.error(f"Failed: {res.text}")

# Display stats
st.subheader("Automation Stats")
col1, col2 = st.columns(2)
col1.metric("Automated Replies", totals["automated"])
col2.metric("Forwarded to Agent", totals["forwarded"])

st.subheader(" Query Type Breakdown")
if query_breakdown:
    st.bar_chart(query_breakdown)
else:
    st.info("No data available yet.")