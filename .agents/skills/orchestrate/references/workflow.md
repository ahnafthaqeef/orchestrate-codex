# Build and escalation workflow

## Build

The parent establishes observable acceptance criteria and inspects the current diff.
Use scout for a bounded code question and researcher for an independent documentation
question when both materially support the implementation. Wait for inputs a change
depends on before assigning it to coder.

Give coder explicit file ownership and the relevant findings. Multiple coders are
useful only with disjoint edits and stable interfaces. A shared checkout requires
coordination; use existing project worktree conventions when isolation is needed.
Do not automatically create, move, or retire worktrees.

Coder runs checks that need build output, generated files, or writable caches under
the inherited sandbox. Scout may inspect results or perform read-only checks. The
parent reviews the integrated diff and verifies the acceptance criteria. Report
unavailable dependencies and skipped checks separately from failures.

## Escalation packet

Supply the architect only the unresolved question, expected and actual behavior,
minimal reproduction, relevant code paths, failed attempts with results, and allowed
tradeoffs. A model change does not add authorization for deployment or data access.
If more effort is needed, the parent obtains the user's approval before a higher-effort pass.
For an approved effort override, account for custom-agent settings taking precedence:
use a generic native agent with the architect remit and the approved settings when
the named agent is pinned to medium; do not claim a spawn override changed a pinned role.

## Result contract

Return: outcome; evidence or changed paths; checks actually run; blockers; next action.
The parent reconciles conflicting results against files and tool evidence. A child
finishing is not proof that its change works. Stop when the requested outcome and
required verification are complete; do not manufacture extra review stages.
