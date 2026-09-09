# Orchestrate Codex

This repository packages a Codex routing skill. Keep it generic and portable.

- For orchestration requests, read `.agents/skills/orchestrate/SKILL.md`. Delegate independent, bounded work when it improves the outcome; handle small or serial tasks directly.
- The main agent owns scope, dependency ordering, integration, and the final report. Each editing agent owns an explicit file set. Do not edit the same files concurrently.
- Preserve existing user changes. Keep credentials, private memories, internal resumes, and personal data out of this bundle.
- New repositories default to private. Before pushing, verify the destination using `gh repo view <owner>/<repo> --json visibility,isPrivate`. Do not change visibility without the user's instruction.
- Use recoverable removal only. Hash-check duplicates before removing copies. Do not relocate worktrees manually.
- Do not introduce SDK calls, API credentials, paid services, or global configuration changes as part of routing.
- Validate changes with `python scripts/validate.py`. Check Codex configuration documentation before changing supported fields. Do not claim schema checks prove live model dispatch.
- Write clear, concise output without em dashes.
