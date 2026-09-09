# Orchestrate Codex

A Codex adaptation of [orchestrate-claude-skill](https://github.com/ahnafthaqeef/orchestrate-claude-skill).
Split suitable work among four roles, keep integration with the main agent, and
escalate difficult problems deliberately. Runs through native Codex subagents with
your existing sign-in. No API server, SDK, or extra API key is required by this bundle.

## Roles

| Role | Model | Effort |
|---|---|---|
| Scout | GPT-5.6 Luna | low |
| Researcher | GPT-5.6 Terra | medium |
| Coder | GPT-5.6 Sol | high |
| Architect | GPT-6 Astra | medium initially |

The main agent retains your selected model. Defaults are starting points, not a
promise of savings. Delegation adds token and coordination overhead, so simple work
stays inline. The architect is reserved for unresolved problems; a higher-effort
retry requires your approval, matching the original bundle's escalation convention.

## Use in this repository

Open this folder in Codex and trust its project configuration only after reviewing it.
Start a fresh session if needed, then invoke:

```text
$orchestrate Map the CLI entry points and independently research the config format.
$orchestrate build Add CSV export to the reports page and verify the exported values.
$orchestrate escalate Investigate this race after the attached ordinary fix failed.
```

## Add to another project

1. Copy `.agents/skills/orchestrate/` into that project's `.agents/skills/`.
2. Copy the four `.codex/agents/*.toml` files into its `.codex/agents/` after checking for name collisions.
3. Merge the `[agents]` settings from `.codex/config.toml` into its existing config. Do not overwrite the whole file.
4. Optionally add this sentence to the project's existing `AGENTS.md`:

   > Use the orchestrate skill for multi-part work with useful independent subtasks; delegate those subtasks and handle small or serial work directly.

Keep your project's existing operating manual. The `AGENTS.md` here governs this
bundle and is not a replacement for an organisation's private instructions.

## Compatibility and configuration

Targets current Codex clients with standalone custom agent TOML discovery. Agent
files contain `name`, `description`, `developer_instructions`, model, and effort.
Skill-only installation also works: when named agents are unavailable, the skill
uses exposed native spawn controls or discloses a sequential fallback.

Model availability depends on the account and host. Select supported pairs in the
agent TOMLs before use. A custom agent file's model/effort can override spawn values;
for an approved deeper architect pass, the workflow explains the generic-agent path.
Read-only role settings are defaults, not a guarantee against live permission
overrides. Parent and host permissions always apply.

Older clients may not support these configuration fields or newer models. Upgrade
or use the skill's sequential fallback. Installing this bundle does not change your
global Codex config, billing, credentials, or existing Claude setup.

## Validate

With Python 3.11 or newer:

```text
python scripts/validate.py
```

This checks TOML structure, role consistency, and packaged references. It does not
authenticate models or prove runtime dispatch. For a live smoke check, ask Codex to
delegate two independent read-only questions about a disposable project, wait for
both, and inspect the reported agent model settings and evidence. No live application
or credential is needed for that check.

## References and license

- [Official subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Official skill discovery and authoring](https://learn.chatgpt.com/docs/build-skills)
- [Original Claude bundle](https://github.com/ahnafthaqeef/orchestrate-claude-skill)

MIT, preserving the original author's copyright. Adapted for Codex in September 2026.
