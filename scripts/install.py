"""Install Orchestrate Codex as a user-wide, default routing workflow."""
from __future__ import annotations

import argparse
import filecmp
import os
from pathlib import Path
import shutil
import sys


ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- orchestrate-codex:begin -->"
END = "<!-- orchestrate-codex:end -->"
DEFAULT_BLOCK = f"""{BEGIN}
## Orchestrate Codex default routing

Before acting on each request, read and apply the installed `orchestrate` skill.
Keep small or serial work with the main agent. Delegate useful independent, bounded
work to the skill's roles, while the main agent owns integration and verification.
The architect is escalation-only and inherits the session model and reasoning effort.
GPT-6 Astra at low effort may proceed normally. Before every architect launch or
retry with GPT-6 Astra at medium effort or higher, remind the user about the elevated
effort and obtain two separate explicit confirmations; earlier task approval does
not count. The user may bypass orchestration for one turn with "skip orchestrate"
or "do it directly".
{END}
"""


def same_tree(source: Path, destination: Path) -> bool:
    source_entries = {path.relative_to(source): path.is_dir() for path in source.rglob("*")}
    destination_entries = {path.relative_to(destination): path.is_dir() for path in destination.rglob("*")}
    if source_entries != destination_entries:
        return False
    return all(
        is_directory or filecmp.cmp(source / relative, destination / relative, shallow=False)
        for relative, is_directory in source_entries.items()
    )


def same_path(source: Path, destination: Path) -> bool:
    if source.is_dir() and destination.is_dir():
        return same_tree(source, destination)
    return source.is_file() and destination.is_file() and filecmp.cmp(source, destination, shallow=False)


def merge_default_block(existing: str) -> str:
    if BEGIN in existing or END in existing:
        if existing.count(BEGIN) != 1 or existing.count(END) != 1:
            raise ValueError("AGENTS.md contains incomplete or duplicate Orchestrate markers")
        start = existing.index(BEGIN)
        finish = existing.index(END, start) + len(END)
        replacement = DEFAULT_BLOCK.rstrip("\n")
        return existing[:start] + replacement + existing[finish:]
    prefix = existing.rstrip()
    return (prefix + "\n\n" if prefix else "") + DEFAULT_BLOCK


def install(home: Path, codex_home: Path) -> None:
    source_skill = ROOT / ".agents" / "skills" / "orchestrate"
    target_skill = home / ".agents" / "skills" / "orchestrate"
    source_agents = sorted((ROOT / ".codex" / "agents").glob("*.toml"))
    target_agents = codex_home / "agents"

    planned = [(source_skill, target_skill)] + [
        (source, target_agents / source.name) for source in source_agents
    ]
    conflicts = [str(target) for source, target in planned if target.exists() and not same_path(source, target)]
    if conflicts:
        raise FileExistsError("Conflicting local files; review them before installation:\n- " + "\n- ".join(conflicts))

    override_md = codex_home / "AGENTS.override.md"
    use_override = override_md.exists() and override_md.read_text(encoding="utf-8").strip()
    agents_md = override_md if use_override else codex_home / "AGENTS.md"
    existing_agents = agents_md.read_text(encoding="utf-8") if agents_md.exists() else ""
    merged_agents = merge_default_block(existing_agents)

    if not target_skill.exists():
        target_skill.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_skill, target_skill)
    target_agents.mkdir(parents=True, exist_ok=True)
    for source in source_agents:
        target = target_agents / source.name
        if not target.exists():
            shutil.copy2(source, target)
    codex_home.mkdir(parents=True, exist_ok=True)
    if merged_agents != existing_agents:
        agents_md.write_text(merged_agents, encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home(), help="User home directory")
    parser.add_argument("--codex-home", type=Path, help="Codex home; defaults to CODEX_HOME or <home>/.codex")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    codex_home = args.codex_home or Path(os.environ.get("CODEX_HOME", args.home / ".codex"))
    try:
        install(args.home.expanduser().resolve(), codex_home.expanduser().resolve())
    except (FileExistsError, ValueError) as exc:
        print(f"Installation conflict: {exc}", file=sys.stderr)
        return 2
    print("Orchestrate Codex installed as the user-wide default. Start a new Codex session.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
