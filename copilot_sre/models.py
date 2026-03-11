from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Alert:
    name: str
    severity: str
    fired_at: str
    summary: str


@dataclass(slots=True)
class MetricPoint:
    timestamp: str
    name: str
    value: float
    baseline: float
    unit: str


@dataclass(slots=True)
class LogEvent:
    timestamp: str
    level: str
    service: str
    message: str


@dataclass(slots=True)
class DeployEvent:
    timestamp: str
    service: str
    version: str
    actor: str
    summary: str


@dataclass(slots=True)
class CommitRef:
    sha: str
    author: str
    message: str


@dataclass(slots=True)
class PullRequestRef:
    number: int
    title: str
    author: str
    state: str
    updated_at: str
    url: str


@dataclass(slots=True)
class Runbook:
    title: str
    path: str
    summary: str


@dataclass(slots=True)
class Incident:
    incident_id: str
    title: str
    service: str
    started_at: str
    customer_impact: str
    symptoms: list[str]
    alerts: list[Alert]
    metrics: list[MetricPoint]
    logs: list[LogEvent]
    deploys: list[DeployEvent]
    commits: list[CommitRef]
    pull_requests: list[PullRequestRef]
    runbooks: list[Runbook]


def _coerce_list(items: list[dict[str, Any]], cls: Any) -> list[Any]:
    return [cls(**item) for item in items]


def incident_from_dict(data: dict[str, Any]) -> Incident:
    return Incident(
        incident_id=data["incident_id"],
        title=data["title"],
        service=data["service"],
        started_at=data["started_at"],
        customer_impact=data["customer_impact"],
        symptoms=list(data.get("symptoms", [])),
        alerts=_coerce_list(data.get("alerts", []), Alert),
        metrics=_coerce_list(data.get("metrics", []), MetricPoint),
        logs=_coerce_list(data.get("logs", []), LogEvent),
        deploys=_coerce_list(data.get("deploys", []), DeployEvent),
        commits=_coerce_list(data.get("commits", []), CommitRef),
        pull_requests=_coerce_list(data.get("pull_requests", []), PullRequestRef),
        runbooks=_coerce_list(data.get("runbooks", []), Runbook),
    )
