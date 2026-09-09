---
name: orchestrate
description: Route multi-part Codex work across scout, researcher, coder, and architect roles, with bounded parallel delegation and controlled escalation. Use for orchestration, parallel work, or builds that benefit from distinct work streams; handle trivial tasks directly.
---

# Orchestrate

Keep planning and final integration with the main agent. Use native Codex subagents
for independent work that benefits from a separate context. This skill requests
delegation for those units; it does not require agents for every task.

## Route

| Role | Default model / effort | Assignment |
|---|---|---|
| scout | gpt-5.6-luna / low | Targeted recon, extraction, code mapping |
| researcher | gpt-5.6-terra / medium | Source verification, comparisons, drafts returned to parent |
| coder | gpt-5.6-sol / high | Scoped implementation and relevant checks |
| architect | gpt-6-astra / medium | One unresolved hard problem after a normal attempt |

These are configurable starting choices, not a measured price or quality ranking.
Keep an explicitly selected user model or budget. Use only model and effort pairs
available on the current host. Read this skill's [workflow](references/workflow.md)
for a multi-stage build or escalation.

## Execute

1. Identify the outcome and split only at meaningful dependency or ownership boundaries.
2. State the intended delegation briefly. Keep small and serial work inline.
3. Prefer the named custom agents when the host exposes them. If only generic native
   spawning is available, pass the role's remit and supported model/effort explicitly.
   Respect the spawn API's context-fork restrictions for model overrides. If overrides
   are unavailable, inherit the parent and disclose that model routing was not applied.
4. Spawn at most three children at once, or fewer if the host limit is smaller.
   Each child needs an objective, relevant context, allowed paths, constraints,
   acceptance evidence, and a concise expected result. Children do not fan out again.
5. Keep useful independent work with the parent. Serialize dependent work and shared
   file edits. Collect every assigned result before claiming completion.
6. Verify integrated behavior and report the outcome, relevant checks, and blockers.

If native delegation is unavailable, execute sequentially and say so. Do not replace
it with API calls, external coding services, or new user-visible tasks.

## Escalation

Correct missing context or a setup error at the same level first. Escalate only the
unresolved reasoning problem, carrying the evidence and failed attempts with it.
After an unsuccessful architect medium pass, explain the remaining problem and ask
before a higher-effort architect run. This is this bundle's usage-control convention,
not a Codex platform requirement. Keep any approval already granted for the same run.
Permission failures are returned to the parent, never treated as a reason to use a
stronger model or weaker sandbox.
