# Copilot SRE Demo Script

## One-line pitch

"Copilot SRE turns GitHub Copilot CLI into an incident commander by gathering operational evidence before Copilot starts reasoning."

## Audience outcome

By the end of the demo, the audience should believe:

- this is more than prompt engineering
- Copilot CLI can become part of real incident response
- the product naturally extends GitHub and Azure workflows

## Demo flow

### 0. Launch the UI

```bash
python -m copilot_sre ui --incident samples/incident-001 --host 127.0.0.1 --port 8765
```

Open `http://127.0.0.1:8765`.

Click `Play Guided Demo` to let the UI automatically narrate and highlight the workflow.

The Azure field is preloaded with a demo App Insights id so the dashboard can render rich telemetry without requiring credentials during the presentation. If you have a real App Insights app id and API key, you can replace it live.

Say:

"This is a local incident cockpit built on top of Copilot CLI. The key idea is that Copilot should reason over an operational brief, not over scattered tools."

## 60-Second Narration

"Copilot SRE turns GitHub Copilot CLI into an incident commander. Instead of starting with a blank prompt during an outage, it assembles the evidence first: alerts, latency regressions, logs, deploy history, runbooks, and live GitHub activity. On this screen you can see the system rank likely root causes, suggest immediate mitigations, and make a rollback recommendation with explicit verification steps. Then it generates a structured Copilot brief so Copilot reasons over real operational context instead of scattered fragments. The result is a workflow that feels native to GitHub and Azure: telemetry comes in, repository activity is correlated, and Copilot becomes much more useful in the highest-pressure engineering moments."

### 1. Set the scene

Say:

"Imagine an on-call engineer gets paged for a checkout outage. The hard part is not asking Copilot a question. The hard part is assembling the right evidence fast enough."

### 2. Run triage

```bash
python -m copilot_sre triage --incident samples/incident-001
```

What to point out:

- severity is derived automatically
- suspects are ranked, not dumped
- next actions are operational, not generic

### 3. Show the timeline

```bash
python -m copilot_sre timeline --incident samples/incident-001
```

Say:

"This connects the deploy, logs, and alerts into a single narrative. Now the operator has incident context, not just telemetry fragments."

### 4. Show the live GitHub correlation

```bash
python -m copilot_sre enrich-github --incident samples/incident-001 --repo github/copilot-cli-for-beginners --lookback-hours 24
python -m copilot_sre triage --incident samples/incident-001
```

Say:

"Now we’re correlating the incident with live repository activity. This is where terminal AI starts to become an actual ops workflow."

### 5. Show mitigation and rollback guidance

```bash
python -m copilot_sre mitigate --incident samples/incident-001
python -m copilot_sre rollback --incident samples/incident-001
```

What to point out:

- it recommends concrete operator actions
- rollback is treated as a decision with rationale and verification, not a generic suggestion

### 6. Show the Copilot prompt

```bash
python -m copilot_sre prompt --incident samples/incident-001
```

What to point out:

- Copilot gets a complete investigation brief
- uncertainty is preserved
- the output request is shaped for incident response: root cause, mitigation, safest next action, verification plan

### 7. Optional live Copilot handoff

```bash
python -m copilot_sre prompt --incident samples/incident-001 --run-copilot
```

Say:

"Copilot SRE does not replace Copilot CLI. It upgrades the quality of the context Copilot reasons over."

## Strong closing line

"The next frontier for terminal agents is not better chat. It is better operational context. Copilot SRE gives Copilot CLI the incident context layer it is missing today."

## Fast UI walkthrough

- Top row: severity, top suspect, and incident context
- Left center: ranked root-cause suspects with confidence-style scoring
- Middle center: mitigation options
- Right center: rollback decision with verification plan
- Lower left: unified timeline
- Lower right: GitHub commits, PRs, runbooks, and alerts
- Bottom: Copilot-ready prompt and live Copilot output

## Extension ideas if asked

- Azure Monitor connector for alert ingestion
- App Insights trace correlation
- GitHub deploy and PR context
- rollback plan generation
- postmortem generation
- recurring incident pattern memory
