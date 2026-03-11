# Evaluation Metrics

## Why evaluation matters

Copilot SRE becomes much more compelling when it is evaluated like an operational product, not just admired like a prototype.

The point is not only that it looks good.

The point is that it should improve the quality and speed of incident handling.

## Core evaluation questions

Copilot SRE should help answer:

- Does it shorten time to understanding?
- Does it improve the quality of early incident hypotheses?
- Does it reduce context-switching across tools?
- Does it make mitigation and rollback decisions clearer?
- Does it improve the quality of the Copilot handoff prompt?

## Recommended metrics

### 1. Time to first plausible root-cause hypothesis

Definition:

How long it takes an engineer to produce a reasonable first explanation for the incident.

Why it matters:

This is one of the most important early indicators of incident response quality.

How to measure:

- baseline: time using standard dashboards + repo browsing only
- experiment: time using Copilot SRE

### 2. Time to mitigation recommendation

Definition:

How long it takes to surface a concrete mitigation plan that an operator could realistically act on.

Why it matters:

Speed matters during active customer impact, but only if the suggested action is credible.

### 3. Time to rollback decision

Definition:

How long it takes to answer:

"Should we roll back now, or continue investigating?"

Why it matters:

Rollback decisions are often high-pressure and expensive. Copilot SRE should make them faster and more evidence-backed.

### 4. Context switches avoided

Definition:

How many separate tools, tabs, or manual context-gathering steps are replaced by the Copilot SRE workflow.

Why it matters:

This measures practical operator friction, not just AI output quality.

Examples:

- switching between alerts, GitHub, logs, runbooks, and docs
- manually summarizing evidence into a prompt

### 5. Incident brief completeness

Definition:

How complete the generated incident brief is compared with a human-prepared incident summary.

Suggested checklist:

- incident title and impact
- likely suspects
- relevant logs
- relevant metrics
- deploy correlation
- repo activity
- runbooks
- mitigation options
- rollback recommendation
- verification steps

### 6. Rollback guidance quality

Definition:

How useful and defensible the rollback recommendation is.

Ways to score:

- did it include rationale?
- did it include verification steps?
- was it directionally correct in hindsight?

### 7. Copilot handoff quality

Definition:

How useful the final structured prompt is when handed to Copilot CLI.

Why it matters:

The whole product depends on increasing the quality of the reasoning input.

Ways to score:

- clarity
- evidence grounding
- operational usefulness
- missing context

## Suggested evaluation format

For a first public version, keep it simple:

### Baseline workflow

- Engineer uses dashboards, logs, GitHub, and notes manually
- Engineer writes a free-form Copilot prompt

### Copilot SRE workflow

- Engineer uses Copilot SRE UI or CLI
- Engineer uses the generated brief and recommendations
- Engineer optionally hands off to Copilot CLI

### Compare

- time to first hypothesis
- time to mitigation recommendation
- time to rollback decision
- number of tools used
- perceived confidence in the decision

## Example evaluation table

| Metric | Baseline | Copilot SRE | Improvement |
|---|---:|---:|---:|
| Time to first hypothesis | 11 min | 4 min | 64% faster |
| Time to mitigation recommendation | 16 min | 6 min | 62% faster |
| Time to rollback decision | 21 min | 8 min | 62% faster |
| Distinct tools used | 5 | 2 | 60% fewer |
| Incident brief completeness | 63% | 92% | +29 pts |

These are example placeholders. Replace them with real observations as you test.

## How to present this to Microsoft

The most persuasive version is:

- one or two realistic incidents
- one baseline run
- one Copilot SRE run
- simple metrics captured consistently

This changes the conversation from:

"This is a cool prototype"

to

"This is a measurable improvement in operational workflow quality"

## One-sentence summary

Copilot SRE should be judged by whether it helps engineers understand incidents faster, act more safely, and hand better context to Copilot CLI.
