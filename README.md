# LabFlow AI 🧪

App link - https://labflow-ai-3cv96pjar7jbmhowx2xh35.streamlit.app/

AI-assisted issue triage for diagnostic-lab software workflows.

## Problem
Operational software issues often arrive as unstructured messages. The first-line investigator needs to understand the workflow, impact and evidence before escalating.

## MVP
Issue → Triage → Investigation checklist → Escalation summary → Issue history

## Features
- Workflow/category classification
- Severity estimation
- Diagnostic signal extraction
- Investigation checklist
- Escalation summary
- Local SQLite issue history

## Tech
Python, Streamlit, SQLite, Pandas, Pytest.

## Run
```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
streamlit run app.py
```

Test:
```bash
pytest
```

## Safety
Synthetic demo data only. Do not enter patient-identifying or confidential healthcare data.

## Product thinking
The MVP intentionally solves the first-mile triage problem rather than trying to automate clinical decisions. Future versions could add an optional LLM layer, team assignment, analytics, ticketing integrations and evaluation metrics.

## Author
Ayan Khan
