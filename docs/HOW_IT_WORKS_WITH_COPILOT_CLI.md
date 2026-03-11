# How Copilot SRE Uses GitHub Copilot CLI

## Short version

Copilot SRE does not replace GitHub Copilot CLI.

It acts as a context and orchestration layer on top of it.

Copilot SRE gathers incident evidence first, structures that evidence into an SRE-grade investigation brief, and then optionally sends that brief to Copilot CLI for reasoning.

## The architecture

There are two layers:

### 1. Copilot SRE

Copilot SRE is responsible for:

- loading incident data
- correlating alerts, logs, deploys, runbooks, metrics, and repo activity
- enriching incidents from GitHub and Application Insights
- ranking likely root causes
- generating mitigation and rollback guidance
- building a structured prompt for incident response
- presenting everything in the UI

In other words, Copilot SRE prepares the operational context.

### 2. GitHub Copilot CLI

Copilot CLI is responsible for:

- taking the final investigation brief
- reasoning over likely root cause and mitigation
- drafting next steps
- producing a response in terminal-friendly form

In other words, Copilot CLI performs the final AI reasoning step after Copilot SRE has assembled the evidence.

## The handoff flow

The flow looks like this:

1. An incident is loaded from an incident pack.
2. Copilot SRE enriches it with GitHub and optionally Azure data.
3. Copilot SRE ranks suspects and generates mitigation and rollback context.
4. Copilot SRE builds a structured prompt.
5. If the operator chooses, Copilot SRE invokes Copilot CLI with that prompt.

## Where this happens in code

### Prompt construction

The incident handoff prompt is built in:

- [prompt_builder.py](../copilot_sre/prompt_builder.py)

That file combines:

- incident summary
- symptoms
- suspects
- recommended actions
- runbooks
- repo activity
- mitigation options
- rollback recommendation
- timeline

into one Copilot-ready brief.

### Copilot invocation

The actual Copilot CLI handoff happens in:

- [copilot_runner.py](../copilot_sre/copilot_runner.py)

That module shells out to:

```bash
copilot -p "<generated prompt>"
```

So the product uses the real Copilot CLI underneath rather than simulating it.

### UI handoff

In the UI flow:

- the dashboard prepares the structured prompt
- the `Run Copilot` button sends that prompt to the backend
- the backend calls `copilot_runner.py`
- the resulting Copilot output is shown in the UI

The UI therefore remains a presentation and orchestration layer, while Copilot CLI remains the underlying reasoning engine.

## Why this matters

The important idea is not "another chat UI."

The important idea is:

Copilot should not start with a vague question during an incident.

It should start with an operational briefing.

That is the value Copilot SRE adds on top of Copilot CLI.

## One-line explanation

Copilot SRE gives GitHub Copilot CLI the incident context layer it needs to reason effectively during real operational events.
