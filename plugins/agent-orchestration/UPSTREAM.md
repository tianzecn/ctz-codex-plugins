# Upstream Sources

This capability plugin combines skills from multiple upstream repositories.

## codex-dynamic-workflows

- Repository: <https://github.com/DannyMac180/skills>
- Imported path: `codex-dynamic-workflows`
- Upstream commit: `5695fa19b9d39b8270025e79633b49a8b863f9a2`
- Local skill: `skills/codex-dynamic-workflows/`

The imported skill records its source commit in its own `SKILL.md`.

## LoopX

- Repository: <https://github.com/huangruiteng/loopx>
- Upstream commit: `0f44cc5299db210589e70349ae1c5f617ce4e510`
- Upstream package version at import: `0.4.4`
- License: MIT; retained in `LICENSE-LOOPX`
- Imported paths: the seven root-level directories under upstream `skills/`

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
