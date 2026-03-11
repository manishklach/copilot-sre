from __future__ import annotations

from .analysis import IncidentAnalysis, MitigationOption, RollbackRecommendation
from .models import Incident


def render_triage(incident: Incident, analysis: IncidentAnalysis) -> str:
    lines = [
        f"Incident {incident.incident_id}: {incident.title}",
        f"Service: {incident.service}",
        f"Severity: {analysis.severity}",
        f"Impact: {incident.customer_impact}",
        "",
        "Top suspects:",
    ]
    for suspect in analysis.suspects:
        lines.append(f"- {suspect.title} [{suspect.score}]")
        lines.append(f"  {suspect.rationale}")

    lines.append("")
    if incident.commits or incident.pull_requests:
        lines.append("Recent repo activity:")
        for commit in incident.commits[:3]:
            lines.append(f"- Commit {commit.sha} by {commit.author}: {commit.message}")
        for pr in incident.pull_requests[:3]:
            lines.append(f"- PR #{pr.number} by {pr.author}: {pr.title} [{pr.state}]")
        lines.append("")
    lines.append("Recommended actions:")
    for action in analysis.recommended_actions:
        lines.append(f"- {action}")
    return "\n".join(lines)


def render_timeline(analysis: IncidentAnalysis) -> str:
    lines = ["Incident timeline:"]
    lines.extend(f"- {entry}" for entry in analysis.timeline)
    return "\n".join(lines)


def render_postmortem_stub(incident: Incident, analysis: IncidentAnalysis) -> str:
    top_suspect = analysis.suspects[0].title if analysis.suspects else "Unknown"
    return f"""# Postmortem: {incident.incident_id} {incident.title}

## Summary
{analysis.summary}

## Customer impact
{incident.customer_impact}

## Likely root cause
{top_suspect}

## Detection
{", ".join(alert.name for alert in incident.alerts)}

## Timeline
{chr(10).join(f"- {entry}" for entry in analysis.timeline)}

## Action items
{chr(10).join(f"- {action}" for action in analysis.recommended_actions)}
""".strip()


def render_mitigation(options: list[MitigationOption]) -> str:
    lines = ["Mitigation plan:"]
    for option in options:
        lines.append(f"- {option.title} [{option.priority}, confidence: {option.confidence}]")
        lines.append(f"  {option.rationale}")
    return "\n".join(lines)


def render_rollback(recommendation: RollbackRecommendation) -> str:
    lines = [
        "Rollback recommendation:",
        f"- Decision: {recommendation.decision}",
        f"- Confidence: {recommendation.confidence}",
        f"- Rationale: {recommendation.rationale}",
        "- Verification steps:",
    ]
    lines.extend(f"  - {step}" for step in recommendation.verification_steps)
    return "\n".join(lines)
