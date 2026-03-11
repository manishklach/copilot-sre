from copilot_sre.azure_connector import enrich_incident_from_app_insights
from copilot_sre.loader import load_incident_dict


def test_enrich_from_app_insights_merges_metrics_and_logs(monkeypatch):
    incident = load_incident_dict("samples/incident-001")

    payloads = [
        {
            "tables": [
                {
                    "columns": [
                        {"name": "timestamp"},
                        {"name": "name"},
                        {"name": "value"},
                        {"name": "baseline"},
                        {"name": "unit"},
                    ],
                    "rows": [
                        ["2026-03-11T10:08:00Z", "appinsights.request_p95", 4200, 430, "ms"],
                        ["2026-03-11T10:09:00Z", "appinsights.failed_request_rate", 12.5, 0.4, "%"],
                    ],
                }
            ]
        },
        {
            "tables": [
                {
                    "columns": [
                        {"name": "timestamp"},
                        {"name": "level"},
                        {"name": "service"},
                        {"name": "message"},
                    ],
                    "rows": [
                        ["2026-03-11T10:07:33Z", "ERROR", "checkout-api", "dependency timeout to payments service"]
                    ],
                }
            ]
        },
    ]

    def fake_query(app_id, api_key, query):
        assert app_id == "app-123"
        assert api_key == "secret"
        return payloads.pop(0)

    monkeypatch.setenv("APPINSIGHTS_API_KEY", "secret")
    monkeypatch.setattr("copilot_sre.azure_connector._query_app_insights", fake_query)

    enriched = enrich_incident_from_app_insights(incident, "app-123", "APPINSIGHTS_API_KEY", 30)

    assert enriched["source_app_insights_app_id"] == "app-123"
    assert any(metric["name"] == "appinsights.request_p95" for metric in enriched["metrics"])
    assert any("dependency timeout" in log["message"] for log in enriched["logs"])

