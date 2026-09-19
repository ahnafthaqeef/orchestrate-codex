"""Validate the portable bundle without network access or third-party packages."""
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def validate():
    config = tomllib.loads((ROOT / '.codex/config.toml').read_text(encoding='utf-8'))
    assert config['agents']['enabled'] is True
    assert config['agents']['max_concurrent_threads_per_session'] == 3
    roles = {}
    for path in sorted((ROOT / '.codex/agents').glob('*.toml')):
        role = tomllib.loads(path.read_text(encoding='utf-8'))
        for key in ('name', 'description', 'developer_instructions'):
            assert isinstance(role.get(key), str) and role[key].strip(), (path, key)
        assert role['name'] == path.stem, path
        assert role['name'] not in roles, path
        if role['name'] == 'architect':
            assert 'model' not in role and 'model_reasoning_effort' not in role, path
        else:
            assert isinstance(role.get('model'), str) and role['model'].strip(), path
            assert role.get('model_reasoning_effort') in {'low', 'medium', 'high'}, path
        if role['name'] != 'coder':
            assert role.get('sandbox_mode') == 'read-only', path
        assert 'approval_policy' not in role, path
        roles[role['name']] = role
    assert set(roles) == {'scout', 'researcher', 'coder', 'architect'}
    skill = ROOT / '.agents/skills/orchestrate/SKILL.md'
    content = skill.read_text(encoding='utf-8')
    assert content.startswith('---\nname: orchestrate\ndescription: ')
    assert len(content.split('---', 2)) == 3
    for role in roles.values():
        if role['name'] != 'architect':
            assert role['model'] in content, role['name']
    assert 'inherit session model / effort' in content
    assert 'two separate' in content
    assert (ROOT / 'scripts/install.py').is_file()
    for path in ROOT.rglob('*.md'):
        if '.git' in path.parts:
            continue
        body = path.read_text(encoding='utf-8')
        assert '\u2014' not in body, path
        for target in re.findall(r'\]\(([^)]+)\)', body):
            if not target.startswith(('https://', 'http://', '#')):
                assert (path.parent / target.split('#')[0]).exists(), (path, target)
    assert (ROOT / 'LICENSE').is_file()
    print('PASS: 4 roles, inherited architect settings, project config, skill metadata, links, and installer')


if __name__ == '__main__':
    validate()
