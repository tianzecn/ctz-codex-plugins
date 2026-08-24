# Upstream provenance

- Repository: https://github.com/hugohe3/ppt-master
- Tag: `v5.0.0`
- Commit: `e469064b0ca85eea179a9af60c9182f7fa8baf1a`
- Imported: 2026-08-24
- Imported skills: 1 (`ppt-master`)
- Deprecated skills skipped: 0
- Upstream package version: `5.0.0`

The plugin imports all 12,922 tracked files from the upstream
`skills/ppt-master/` directory. Of those, 12,911 are preserved byte-for-byte.
The Codex package adds `skills/ppt-master/agents/openai.yaml` for the
user-visible bilingual name and Chinese summary.

Eleven upstream files had trailing whitespace or extra blank lines at EOF that
failed the target repository's mandatory `git diff --check` gate. Packaging
normalizes only that whitespace in seven Python modules, three chart SVGs, and
`scripts/tts_backends/__init__.py`; no executable logic, SVG geometry, prompt,
workflow, template semantics, attribution text, or integrity gate is changed.

The primary upstream license is MIT and remains available at
`skills/ppt-master/LICENSE`. Bundled data, icons, sounds, and brand marks also
carry Apache-2.0, MIT, CC BY 4.0, CC0, attribution, and trademark conditions.
Their original license and notice files remain with the imported assets,
including:

- `scripts/pptx_shapes/data/NOTICE.md`
- `templates/icons/THIRD_PARTY_NOTICES.md`
- `templates/sounds/THIRD_PARTY_NOTICES.md`

The package does not install Python dependencies automatically. Runtime users
must install the dependencies declared in
`skills/ppt-master/requirements.txt` when the selected PPT workflow needs them.
Packaging validation does not read API keys, call model providers, generate a
presentation, or send user content over the network.

No upstream workflow, attribution file, or integrity gate is modified. The
upstream `scripts/attribution_guard.py` passes in the packaged Skill.
