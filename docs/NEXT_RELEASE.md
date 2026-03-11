# Next Release: v0.2.0

## Theme

Move Copilot SRE from polished showcase to believable live-incident workflow.

## Why this release matters

The current version proves the product idea well:

- strong UI
- replayable demo
- GitHub enrichment
- Application Insights demo mode
- mitigation and rollback guidance
- Copilot CLI handoff

The biggest remaining gap is live evidence gathering with minimal setup.

That is what `v0.2.0` should address.

## Release goals

### 1. MCP-backed live evidence gathering

Use MCP as the main path for pulling live context into the incident workflow.

Initial targets:

- GitHub MCP
- filesystem MCP for runbooks
- documentation MCP where useful

### 2. Auto-generated incident packs

Replace more of the hand-curated incident input with automatically assembled evidence:

- alert
- deploy context
- repo activity
- telemetry snapshot
- runbook matches

### 3. Lower setup friction

The path from demo mode to real usage should feel much lighter.

The target experience:

- demo works immediately
- one or two real sources can be connected quickly
- users can still see what evidence was pulled and why

### 4. Stronger operational proof

Add at least one real baseline-vs-Copilot-SRE comparison using the evaluation framework.

## Success criteria

`v0.2.0` is successful if:

- a user can connect at least one live MCP source in minutes
- the system can build a usable incident brief from live context
- the output remains explainable and operator-friendly
- the evaluation story becomes more concrete

## Why this is the right next release

This is the release that can change the project perception from:

- impressive demo

to

- credible product direction

## Related docs

- [MCP_PLAN.md](MCP_PLAN.md)
- [EVALUATION.md](EVALUATION.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
