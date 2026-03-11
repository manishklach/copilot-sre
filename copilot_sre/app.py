from __future__ import annotations

import argparse

from .analysis import analyze_incident, build_mitigation_plan, build_rollback_recommendation
from .azure_connector import enrich_incident_from_app_insights
from .copilot_runner import run_copilot
from .github_connector import enrich_incident_from_github
from .loader import load_incident, load_incident_dict, save_incident_dict
from .prompt_builder import build_prompt
from .render import render_mitigation, render_postmortem_stub, render_rollback, render_timeline, render_triage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="copilot-sre",
        description="Incident commander workflows on top of GitHub Copilot CLI",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name in ("triage", "timeline", "postmortem", "prompt", "mitigate", "rollback"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("--incident", required=True, help="Path to an incident directory")
        if name == "prompt":
            subparser.add_argument(
                "--run-copilot",
                action="store_true",
                help="Send the generated prompt directly to Copilot CLI",
            )
    enrich = subparsers.add_parser("enrich-github")
    enrich.add_argument("--incident", required=True, help="Path to an incident directory")
    enrich.add_argument("--repo", required=True, help="GitHub repository in owner/name format")
    enrich.add_argument("--token-env", default="GITHUB_TOKEN", help="Environment variable containing a GitHub token")
    enrich.add_argument(
        "--lookback-hours",
        type=int,
        default=24,
        help="How far back to look for repo activity relative to incident start",
    )
    azure = subparsers.add_parser("enrich-azure")
    azure.add_argument("--incident", required=True, help="Path to an incident directory")
    azure.add_argument("--app-id", required=True, help="Application Insights app id")
    azure.add_argument("--api-key-env", default="APPINSIGHTS_API_KEY", help="Environment variable containing an App Insights API key")
    azure.add_argument(
        "--lookback-minutes",
        type=int,
        default=30,
        help="How far around incident start to query telemetry",
    )
    ui = subparsers.add_parser("ui")
    ui.add_argument("--incident", required=True, help="Path to an incident directory")
    ui.add_argument("--host", default="127.0.0.1", help="Host to bind")
    ui.add_argument("--port", type=int, default=8765, help="Port to bind")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    incident = load_incident(args.incident)

    if args.command == "enrich-github":
        incident_data = load_incident_dict(args.incident)
        enriched = enrich_incident_from_github(
            incident_data=incident_data,
            repo=args.repo,
            token_env=args.token_env,
            lookback_hours=args.lookback_hours,
        )
        save_incident_dict(args.incident, enriched)
        print(f"Enriched {args.incident} with live GitHub context from {args.repo}.")
        return 0

    if args.command == "enrich-azure":
        incident_data = load_incident_dict(args.incident)
        enriched = enrich_incident_from_app_insights(
            incident_data=incident_data,
            app_id=args.app_id,
            api_key_env=args.api_key_env,
            lookback_minutes=args.lookback_minutes,
        )
        save_incident_dict(args.incident, enriched)
        print(f"Enriched {args.incident} with Application Insights data from app {args.app_id}.")
        return 0

    if args.command == "ui":
        from .web import main as web_main

        return web_main(
            [
                "--incident",
                args.incident,
                "--host",
                args.host,
                "--port",
                str(args.port),
            ]
        )

    analysis = analyze_incident(incident)

    if args.command == "triage":
        print(render_triage(incident, analysis))
        return 0

    if args.command == "timeline":
        print(render_timeline(analysis))
        return 0

    if args.command == "postmortem":
        print(render_postmortem_stub(incident, analysis))
        return 0

    if args.command == "mitigate":
        print(render_mitigation(build_mitigation_plan(incident, analysis)))
        return 0

    if args.command == "rollback":
        print(render_rollback(build_rollback_recommendation(incident, analysis)))
        return 0

    prompt = build_prompt(incident, analysis)
    if args.run_copilot:
        code, output = run_copilot(prompt)
        print(output)
        return code

    print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
