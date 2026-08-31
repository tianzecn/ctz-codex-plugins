# Upstream provenance

- Repository: https://github.com/hugohe3/ppt-master
- Tag: `v6.1.0`
- Commit: `c40bca58e168fcef2facdc7612cc352d1233679b`
- Imported: 2026-08-31
- Imported skills: 1 (`ppt-master`)
- Deprecated skills skipped: 0
- Upstream package version: `6.1.0`
- Release archive: `ppt-master-skill-v6.1.0.zip`
- Release archive SHA-256: `39a33c611e868c507c4d26d1b0c479ddbcb854dd66d30c3e0c5495a37dc5891a`

The plugin imports all 12,939 files from the official release archive's
`skills/ppt-master/` directory. The Codex package adds
`skills/ppt-master/agents/openai.yaml` for the user-visible bilingual name and Chinese summary.

Upstream files with trailing whitespace, CRLF-only line endings, or extra blank lines at EOF are
normalized only when required by the target repository's mandatory `git diff --check` gate. No
executable logic, SVG geometry, prompt, workflow, template semantics, attribution text, or
integrity gate is changed.

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
