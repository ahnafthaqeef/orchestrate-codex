"""Behavior tests for the user-wide installer."""
from pathlib import Path
import os
import shutil
import subprocess
import sys
import uuid


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts" / "install.py"
BEGIN_MARKER = "<!-- orchestrate-codex:begin -->"


def run_installer(home: Path, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["CODEX_HOME"] = str(home / "must-not-be-used")
    result = subprocess.run(
        [
            sys.executable,
            str(INSTALLER),
            "--home",
            str(home),
            "--codex-home",
            str(home / ".codex"),
            *args,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )
    assert result.returncode == expect, result.stdout + result.stderr
    return result


def main() -> None:
    nonce = uuid.uuid4().hex
    home = ROOT / f".test-home-install-{nonce}"
    override_home = ROOT / f".test-home-install-override-{nonce}"
    assert not home.exists() and not override_home.exists()
    home.mkdir()
    try:
        codex_home = home / ".codex"
        codex_home.mkdir()
        agents_md = codex_home / "AGENTS.md"
        agents_md.write_text("# Existing preferences\n\nKeep this line.\n", encoding="utf-8")

        run_installer(home)
        skill = home / ".agents" / "skills" / "orchestrate" / "SKILL.md"
        assert skill.read_text(encoding="utf-8") == (
            ROOT / ".agents" / "skills" / "orchestrate" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for role in ("scout", "researcher", "coder", "architect"):
            assert (codex_home / "agents" / f"{role}.toml").is_file()
        first_agents = agents_md.read_text(encoding="utf-8")
        assert first_agents.startswith("# Existing preferences\n\nKeep this line.\n")
        assert first_agents.count("<!-- orchestrate-codex:begin -->") == 1
        assert "read and apply" in first_agents.lower()
        assert not (home / "must-not-be-used").exists()

        run_installer(home)
        assert agents_md.read_text(encoding="utf-8") == first_agents

        source_scout = ROOT / ".codex" / "agents" / "scout.toml"
        target_scout = codex_home / "agents" / "scout.toml"
        conflicting_bytes = source_scout.read_bytes().replace(b"scout", b"snout", 1)
        assert len(conflicting_bytes) == source_scout.stat().st_size
        target_scout.write_bytes(conflicting_bytes)
        source_times = source_scout.stat()
        os.utime(target_scout, ns=(source_times.st_atime_ns, source_times.st_mtime_ns))
        result = run_installer(home, expect=2)
        assert "conflict" in (result.stdout + result.stderr).lower()
        assert target_scout.read_bytes() == conflicting_bytes

        override_codex = override_home / ".codex"
        override_codex.mkdir(parents=True)
        base_agents = override_codex / "AGENTS.md"
        active_override = override_codex / "AGENTS.override.md"
        base_agents.write_text("base instructions\n", encoding="utf-8")
        active_override.write_text("temporary override\n", encoding="utf-8")
        run_installer(override_home)
        assert base_agents.read_text(encoding="utf-8") == "base instructions\n"
        assert BEGIN_MARKER in active_override.read_text(encoding="utf-8")

    finally:
        shutil.rmtree(home)
        if override_home.exists():
            shutil.rmtree(override_home)

    print("PASS: clean install, preserved instructions, idempotence, and conflict refusal")


if __name__ == "__main__":
    main()
