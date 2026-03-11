# MCP Integration Plan

## Why MCP is the next leverage point

The current incident-pack workflow is ideal for demos and product storytelling.

The next version should make live evidence gathering far easier by letting Copilot SRE pull incident context through MCP-backed sources instead of relying on mostly preassembled data.

That is the transition from:

- showcase prototype

to

- something people could actually run during a live incident

## v0.2.0 goal

Use MCP as the live context ingestion layer for Copilot SRE.

## What v0.2.0 should do

### 1. GitHub MCP integration

Use MCP-backed GitHub context to pull:

- recent commits
- recent pull requests
- deployment or workflow context
- linked issues if relevant

This should reduce the need for custom GitHub API plumbing where MCP is already sufficient.

### 2. Filesystem / runbook MCP integration

Use MCP-backed file access to:

- locate runbooks
- inspect release notes
- find service-specific operational docs
- pull environment or deployment notes where safe

### 3. Documentation MCP integration

Use a documentation-capable MCP source to:

- fetch current guidance for Azure or GitHub workflows
- support operators during unusual failures
- ground follow-up recommendations in current docs

### 4. Incident pack auto-generation

Instead of requiring a hand-curated `incident.json`, v0.2.0 should generate an incident pack from live signals:

- active alert
- telemetry snapshot
- recent repo activity
- matching runbooks
- deployment context

### 5. Zero-config demo-to-live path

The setup experience should aim for:

- demo mode works out of the box
- one or two real MCP sources can be added with minimal setup
- operators can see what was pulled and why

## Success criteria

v0.2.0 is successful if:

- a user can connect at least one live MCP source in minutes
- Copilot SRE can assemble a live incident brief without hand-editing an incident file
- the output is still explainable and operator-friendly
- the GitHub + Azure story becomes stronger, not more brittle

## Suggested implementation order

1. GitHub MCP
2. Filesystem MCP for runbooks
3. Incident pack auto-generation
4. Additional live telemetry or documentation MCP sources

## Why this matters

MCP is the piece that can turn Copilot SRE from a polished showcase into a believable operational product direction.
