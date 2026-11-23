import streamlit as st
from src.analyzer import analyze_issue, build_escalation_summary
from src.db import init_db, save_issue, load_issues

st.set_page_config(page_title="LabFlow AI", page_icon="🧪", layout="wide")
init_db()

st.title("🧪 LabFlow AI")
st.caption("AI-assisted issue triage for diagnostic-lab software workflows")
st.info("Demo only. Use synthetic examples; never enter real patient or confidential data.")

tab1, tab2 = st.tabs(["Analyze an issue", "Issue history"])

with tab1:
    issue = st.text_area(
        "Customer / lab user message",
        height=160,
        placeholder="Example: Since 10:30 AM, samples from the hematology analyzer are reaching the accession queue but results are not appearing in the validation worklist."
    )
    submitted_by = st.text_input("Submitted by", "Demo lab user")
    workflow = st.selectbox(
        "Workflow", ["Auto-detect", "Accession", "Analyzer / Integration",
        "Validation", "Billing", "Inventory", "Patient Portal", "Reporting", "Other"]
    )

    if st.button("Analyze issue", type="primary", use_container_width=True):
        if not issue.strip():
            st.warning("Please describe an issue first.")
        else:
            st.session_state["result"] = analyze_issue(issue, workflow)

    result = st.session_state.get("result")
    if result:
        c1, c2, c3 = st.columns(3)
        c1.metric("Category", result["category"])
        c2.metric("Severity", result["severity"])
        c3.metric("Confidence", f'{result["confidence"]}%')

        left, right = st.columns(2)
        with left:
            st.subheader("What I understood")
            st.write(result["summary"])
            st.subheader("Key signals")
            for item in result["signals"]:
                st.write("• " + item)

        with right:
            st.subheader("Suggested next steps")
            for i, item in enumerate(result["next_steps"], 1):
                st.write(f"{i}. {item}")

        st.subheader("Escalation summary")
        st.code(build_escalation_summary(issue, result))

        if st.button("Save this issue"):
            save_issue(submitted_by, workflow, issue, result)
            st.success("Issue saved.")

with tab2:
    history = load_issues()
    if history.empty:
        st.info("No saved issues yet.")
    else:
        st.dataframe(history, use_container_width=True, hide_index=True)
