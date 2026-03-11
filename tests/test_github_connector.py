from copilot_sre.github_connector import enrich_incident_from_github
from copilot_sre.loader import load_incident_dict


def test_enrich_preserves_incident_and_updates_repo_context(monkeypatch):
    incident = load_incident_dict("samples/incident-001")

    def fake_fetch_commits(repo, since, token):
        assert repo == "octo/example"
        assert since.endswith("Z")
        return [{"sha": "abc1234", "author": "octo", "message": "fix checkout env var"}]

    def fake_fetch_pull_requests(repo, token):
        assert repo == "octo/example"
        return [
            {
                "number": 42,
                "title": "Fix payment base URL",
                "author": "octo",
                "state": "merged",
                "updated_at": "2026-03-11T10:12:00Z",
                "url": "https://github.com/octo/example/pull/42",
            }
        ]

    monkeypatch.setattr("copilot_sre.github_connector._fetch_commits", fake_fetch_commits)
    monkeypatch.setattr("copilot_sre.github_connector._fetch_pull_requests", fake_fetch_pull_requests)

    enriched = enrich_incident_from_github(incident, "octo/example", "GITHUB_TOKEN", 24)

    assert enriched["source_repo"] == "octo/example"
    assert enriched["commits"][0]["sha"] == "abc1234"
    assert enriched["pull_requests"][0]["number"] == 42
