from copilot_sre.analysis import analyze_incident
from copilot_sre.loader import load_incident


def test_triage_prioritizes_recent_deploy():
    incident = load_incident("samples/incident-001")
    analysis = analyze_incident(incident)

    assert analysis.severity == "high"
    assert analysis.suspects[0].title.startswith("Recent deploy")
    assert any("rollback" in action.lower() for action in analysis.recommended_actions)
