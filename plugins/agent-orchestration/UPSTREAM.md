# Upstream Sources

This capability plugin combines skills from multiple upstream repositories.

## codex-dynamic-workflows

- Repository: <https://github.com/DannyMac180/skills>
- Imported path: `codex-dynamic-workflows`
- Upstream commit: `ae9af55a3ad9ee396d6edcc9177c6f83638e73f4`
- Local skill: `skills/codex-dynamic-workflows/`

The imported skill records its source commit in its own `SKILL.md`.

## LoopX

- Repository: <https://github.com/huangruiteng/loopx>
- Release: `v0.5.3`
- Upstream commit: `c49a4e116d0a4eece27377032fb1641e08b0ef75`
- Upstream package version at import: `0.5.3`
- License: MIT; retained in `LICENSE-LOOPX`
- Imported paths: the eight root-level directories under upstream `skills/`

The package-internal Auto Research worker skill and the Claude Code-specific
adapter were not imported because neither is a root-level Codex skill entry.
The LoopX Python runtime is not bundled; users must install the `loopx` CLI
separately.

The imported LoopX skill resources are unchanged except for:

- natural Chinese `display_name` and `short_description` values in
  `agents/openai.yaml`;
- Codex authorization-boundary adjustments requiring explicit current-task
  user approval before publishing PR reviews or issues, or creating commits,
  pushes, or pull requests.
