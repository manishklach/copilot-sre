from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from typing import Any


TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DEMO_APP_ID = "cf58dcfd-0683-487c-bc84-048789bca8e5"
DEMO_APP_ALIAS = "demo-fabrikam-appinsights"


def _query_app_insights(app_id: str, api_key: str, query: str) -> dict[str, Any]:
    encoded = urllib.parse.urlencode({"query": query})
    url = f"https://api.applicationinsights.io/v1/apps/{app_id}/query?{encoded}"
    request = urllib.request.Request(url)
    request.add_header("x-api-key", api_key)
    request.add_header("Accept", "application/json")
    request.add_header("User-Agent", "copilot-sre")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _rows_to_dicts(table: dict[str, Any]) -> list[dict[str, Any]]:
    columns = [column["name"] for column in table.get("columns", [])]
    return [dict(zip(columns, row)) for row in table.get("rows", [])]


def _extract_first_table(payload: dict[str, Any]) -> list[dict[str, Any]]:
    tables = payload.get("tables", [])
    if not tables:
        return []
    return _rows_to_dicts(tables[0])


def _build_metric_entries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    metrics: list[dict[str, Any]] = []
    for row in rows:
        metrics.append(
            {
                "timestamp": row.get("timestamp", ""),
                "name": row.get("name", ""),
                "value": float(row.get("value", 0)),
                "baseline": float(row.get("baseline", 0)),
                "unit": row.get("unit", ""),
            }
        )
    return metrics


def _build_log_entries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    logs: list[dict[str, Any]] = []
    for row in rows:
        logs.append(
            {
                "timestamp": row.get("timestamp", ""),
                "level": row.get("level", "INFO"),
                "service": row.get("service", "application-insights"),
                "message": row.get("message", ""),
            }
        )
    return logs


def _incident_window(started_at: str, lookback_minutes: int) -> tuple[str, str]:
    start = datetime.strptime(started_at, TIME_FORMAT)
    begin = start - timedelta(minutes=lookback_minutes)
    end = start + timedelta(minutes=lookback_minutes)
    return begin.strftime(TIME_FORMAT), end.strftime(TIME_FORMAT)


def _is_demo_app(app_id: str) -> bool:
    return app_id in {DEMO_APP_ID, DEMO_APP_ALIAS, "demo", "demo-app"}


def _demo_metrics() -> list[dict[str, Any]]:
    return [
        {"timestamp": "2026-03-11T09:50:00Z", "name": "appinsights.request_p95", "value": 430, "baseline": 420, "unit": "ms"},
        {"timestamp": "2026-03-11T09:55:00Z", "name": "appinsights.request_p95", "value": 510, "baseline": 420, "unit": "ms"},
        {"timestamp": "2026-03-11T10:00:00Z", "name": "appinsights.request_p95", "value": 770, "baseline": 420, "unit": "ms"},
        {"timestamp": "2026-03-11T10:05:00Z", "name": "appinsights.request_p95", "value": 1280, "baseline": 420, "unit": "ms"},
        {"timestamp": "2026-03-11T10:10:00Z", "name": "appinsights.request_p95", "value": 3920, "baseline": 420, "unit": "ms"},
        {"timestamp": "2026-03-11T10:15:00Z", "name": "appinsights.request_p95", "value": 3670, "baseline": 420, "unit": "ms"},
        {"timestamp": "2026-03-11T09:50:00Z", "name": "appinsights.failed_request_rate", "value": 0.3, "baseline": 0.2, "unit": "%"},
        {"timestamp": "2026-03-11T09:55:00Z", "name": "appinsights.failed_request_rate", "value": 0.4, "baseline": 0.2, "unit": "%"},
        {"timestamp": "2026-03-11T10:00:00Z", "name": "appinsights.failed_request_rate", "value": 1.2, "baseline": 0.2, "unit": "%"},
        {"timestamp": "2026-03-11T10:05:00Z", "name": "appinsights.failed_request_rate", "value": 3.7, "baseline": 0.2, "unit": "%"},
        {"timestamp": "2026-03-11T10:10:00Z", "name": "appinsights.failed_request_rate", "value": 12.8, "baseline": 0.2, "unit": "%"},
        {"timestamp": "2026-03-11T10:15:00Z", "name": "appinsights.failed_request_rate", "value": 10.4, "baseline": 0.2, "unit": "%"},
        {"timestamp": "2026-03-11T09:50:00Z", "name": "appinsights.checkout_conversion_rate", "value": 72.0, "baseline": 72.0, "unit": "%"},
        {"timestamp": "2026-03-11T09:55:00Z", "name": "appinsights.checkout_conversion_rate", "value": 71.0, "baseline": 72.0, "unit": "%"},
        {"timestamp": "2026-03-11T10:00:00Z", "name": "appinsights.checkout_conversion_rate", "value": 68.0, "baseline": 72.0, "unit": "%"},
        {"timestamp": "2026-03-11T10:05:00Z", "name": "appinsights.checkout_conversion_rate", "value": 59.0, "baseline": 72.0, "unit": "%"},
        {"timestamp": "2026-03-11T10:10:00Z", "name": "appinsights.checkout_conversion_rate", "value": 41.0, "baseline": 72.0, "unit": "%"},
        {"timestamp": "2026-03-11T10:15:00Z", "name": "appinsights.checkout_conversion_rate", "value": 44.0, "baseline": 72.0, "unit": "%"},
    ]


def _demo_logs() -> list[dict[str, Any]]:
    return [
        {"timestamp": "2026-03-11T10:04:51Z", "level": "WARN", "service": "checkout-api", "message": "new payment endpoint rollout reached 100% of production traffic"},
        {"timestamp": "2026-03-11T10:06:18Z", "level": "ERROR", "service": "checkout-api", "message": "dependency call to payments-v2.internal exceeded 5s timeout budget"},
        {"timestamp": "2026-03-11T10:07:02Z", "level": "ERROR", "service": "checkout-api", "message": "dependency failure cluster detected in westus checkout ring"},
        {"timestamp": "2026-03-11T10:08:19Z", "level": "CRITICAL", "service": "payments-api", "message": "payment endpoint configuration mismatch between checkout-api and payments-api"},
        {"timestamp": "2026-03-11T10:09:54Z", "level": "ERROR", "service": "checkout-api", "message": "retry storm detected for payment authorization workflow"},
    ]


def _demo_dashboard() -> dict[str, Any]:
    return {
        "headline": "Demo App Insights: checkout health collapsed immediately after dependency endpoint rollout",
        "kpis": [
            {"label": "P95 latency", "value": "3.92s", "delta": "+833%", "tone": "critical"},
            {"label": "Failed requests", "value": "12.8%", "delta": "+12.6 pts", "tone": "critical"},
            {"label": "Checkout conversion", "value": "41%", "delta": "-31 pts", "tone": "warning"},
            {"label": "Dependency errors", "value": "5x", "delta": "spike", "tone": "critical"},
        ],
        "narrative": [
            "Latency begins drifting at 10:00 UTC, then spikes after the 10:05 rollout.",
            "Request failures climb in lockstep with dependency timeout and retry-storm logs.",
            "Conversion rate drops sharply, indicating direct business impact instead of an internal-only regression.",
        ],
    }


def _build_metric_query(service: str, begin: str, end: str) -> str:
    return f"""
let startTime = datetime({begin});
let endTime = datetime({end});
let req = requests
| where timestamp between (startTime .. endTime)
| where cloud_RoleName == "{service}" or operation_Name contains "{service}"
| summarize failed=countif(success == false), total=count(), p95=percentile(duration, 95) by bin(timestamp, 5m);
let base = requests
| where timestamp between (startTime - 1d .. endTime - 1d)
| where cloud_RoleName == "{service}" or operation_Name contains "{service}"
| summarize baseline_p95=percentile(duration, 95), baseline_failed=countif(success == false) * 100.0 / count() by bin(timestamp, 5m);
req
| join kind=leftouter base on timestamp
| project timestamp, name="appinsights.request_p95", value=todouble(p95), baseline=todouble(baseline_p95), unit="ms"
| union (
    req
    | join kind=leftouter base on timestamp
    | extend failed_rate = iff(total == 0, 0.0, failed * 100.0 / total)
    | project timestamp, name="appinsights.failed_request_rate", value=todouble(failed_rate), baseline=todouble(baseline_failed), unit="%"
)
| top 6 by timestamp desc
""".strip()


def _build_log_query(service: str, begin: str, end: str) -> str:
    return f"""
let startTime = datetime({begin});
let endTime = datetime({end});
union traces, exceptions
| where timestamp between (startTime .. endTime)
| where cloud_RoleName == "{service}" or operation_Name contains "{service}" or appName contains "{service}"
| extend level = case(severityLevel >= 3, "ERROR", severityLevel == 2, "WARN", "INFO")
| extend service = iff(isempty(cloud_RoleName), "{service}", cloud_RoleName)
| extend message = coalesce(message, outerMessage, innermostMessage, problemId)
| where isnotempty(message)
| project timestamp, level, service, message
| top 8 by timestamp desc
""".strip()


def enrich_incident_from_app_insights(
    incident_data: dict[str, Any],
    app_id: str,
    api_key_env: str,
    lookback_minutes: int,
) -> dict[str, Any]:
    if _is_demo_app(app_id):
        enriched = dict(incident_data)
        enriched["source_app_insights_app_id"] = app_id
        enriched["app_insights_demo"] = True
        enriched["app_insights_dashboard"] = _demo_dashboard()
        enriched["metrics"] = _demo_metrics()
        existing_logs = incident_data.get("logs", [])
        existing_messages = {entry.get("message") for entry in existing_logs}
        demo_logs = [entry for entry in _demo_logs() if entry["message"] not in existing_messages]
        enriched["logs"] = existing_logs + demo_logs
        return enriched

    api_key = os.environ.get(api_key_env)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {api_key_env}")

    begin, end = _incident_window(incident_data["started_at"], lookback_minutes)
    service = incident_data["service"]

    try:
        metric_rows = _extract_first_table(_query_app_insights(app_id, api_key, _build_metric_query(service, begin, end)))
        log_rows = _extract_first_table(_query_app_insights(app_id, api_key, _build_log_query(service, begin, end)))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Application Insights query failed with status {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Application Insights query failed: {exc.reason}") from exc

    enriched = dict(incident_data)
    enriched["source_app_insights_app_id"] = app_id
    enriched["app_insights_demo"] = False
    enriched["metrics"] = _build_metric_entries(metric_rows) or incident_data.get("metrics", [])
    existing_logs = incident_data.get("logs", [])
    existing_messages = {entry.get("message") for entry in existing_logs}
    new_logs = [entry for entry in _build_log_entries(log_rows) if entry["message"] not in existing_messages]
    enriched["logs"] = existing_logs + new_logs
    return enriched
