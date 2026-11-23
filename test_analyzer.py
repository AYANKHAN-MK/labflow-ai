from src.analyzer import analyze_issue

def test_analyzer_category():
    r = analyze_issue("The hematology analyzer is connected but results are not appearing.")
    assert r["category"] == "Analyzer / Integration"

def test_high_severity():
    r = analyze_issue("The entire lab is down and cannot process samples.")
    assert r["severity"] == "High"
