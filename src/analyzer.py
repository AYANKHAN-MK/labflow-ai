import re

CATEGORY_RULES = {
    "Analyzer / Integration": ["analyzer", "instrument", "hl7", "fhir", "middleware", "interface", "integration"],
    "Accession": ["accession", "barcode", "sample received", "collection", "specimen"],
    "Validation": ["validation", "rule engine", "delta check", "critical value", "approval", "approve result"],
    "Billing": ["invoice", "billing", "claim", "payment", "charge", "revenue"],
    "Inventory": ["reagent", "stock", "inventory", "purchase order", "consumption"],
    "Patient Portal": ["patient portal", "patient login", "appointment", "report download"],
    "Reporting": ["report", "dashboard", "export", "analytics", "mis"],
}

def classify_category(text, workflow="Auto-detect"):
    if workflow != "Auto-detect":
        return workflow, 90
    scores = {c: sum(k in text.lower() for k in keys) for c, keys in CATEGORY_RULES.items()}
    category, score = max(scores.items(), key=lambda x: x[1])
    return (category, min(95, 60 + score * 8)) if score else ("Other", 45)

def classify_severity(text):
    t = text.lower()
    if any(x in t for x in ["all samples", "entire lab", "outage", "down", "blocked", "stopped", "no results"]):
        return "High"
    if any(x in t for x in ["multiple", "delayed", "intermittent", "missing", "failed", "slow"]):
        return "Medium"
    return "Low"

def extract_signals(text):
    signals = []
    t = text.lower()
    if re.search(r"\b\d{1,2}:\d{2}\b", text):
        signals.append("A specific time was provided.")
    if any(x in t for x in ["all samples", "entire lab", "multiple"]):
        signals.append("The reported impact may affect more than one record or user.")
    if any(x in t for x in ["not appearing", "missing", "delayed"]):
        signals.append("The issue suggests a data-flow or processing gap.")
    if any(x in t for x in ["analyzer", "hl7", "fhir", "middleware"]):
        signals.append("An external-system or integration boundary may be involved.")
    return signals or ["The description needs more diagnostic detail."]

def next_steps_for(category, severity):
    common = [
        "Confirm the exact start time and whether the issue is still reproducible.",
        "Check whether the problem affects one record, one user, or multiple workflows.",
        "Capture a representative record ID and the exact error/message if available."
    ]
    specific = {
        "Analyzer / Integration": ["Check the integration/middleware queue for rejected or delayed messages.",
                                   "Compare one affected result with a recent successful result."],
        "Accession": ["Verify barcode/sample status and the last successful accession event.",
                      "Check whether affected samples are visible in the expected queue."],
        "Validation": ["Review the validation rule or workflow step that should have processed the result.",
                       "Compare the affected result with a known-good result."],
        "Billing": ["Verify the source transaction and downstream billing status.",
                    "Check whether the issue is isolated to one account, invoice, or workflow."],
        "Inventory": ["Verify the item, current stock state, and most recent inventory event.",
                      "Check whether the discrepancy is isolated to one location or item."],
        "Patient Portal": ["Reproduce using a non-sensitive test account.",
                           "Check the relevant API/workflow status and browser-facing error."],
        "Reporting": ["Compare report output with the underlying source records.",
                      "Check whether the discrepancy is caused by refresh, filter, or transformation."],
        "Other": ["Identify the exact workflow step where expected behavior diverges.",
                  "Collect one successful example and one affected example for comparison."]
    }
    steps = specific.get(category, specific["Other"])
    return (["Assess current business impact and identify a safe workaround if available."] + steps + common
            if severity == "High" else steps + common)

def analyze_issue(text, workflow="Auto-detect"):
    category, confidence = classify_category(text, workflow)
    severity = classify_severity(text)
    return {
        "category": category,
        "severity": severity,
        "confidence": confidence,
        "summary": f"The issue appears to involve {category.lower()} with {severity.lower()} severity based on the information provided.",
        "signals": extract_signals(text),
        "next_steps": next_steps_for(category, severity)
    }

def build_escalation_summary(issue, result):
    return (
        f"Category: {result['category']}\n"
        f"Severity: {result['severity']}\n"
        f"Confidence: {result['confidence']}%\n\n"
        f"Reported issue:\n{issue.strip()}\n\n"
        "Suggested investigation:\n" +
        "\n".join("- " + x for x in result["next_steps"])
    )
