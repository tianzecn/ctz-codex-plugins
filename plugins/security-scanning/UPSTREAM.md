# Upstream provenance

- Repository: <https://github.com/zhaoxuya520/reverse-skill>
- Release: `v1.0.1`
- Imported commit: `9c28c6ca1062a1a076e28baf40f241dbb4cf5dc2`
- Imported on: 2026-08-31
- Main package version file: `1.0.1`
- Imported discoverable skills: 85

The upstream repository rewrote history after the previous import, so the old and new commits have
no common ancestor. This update rebuilds the declared package from the v1.0.1 release instead of
pretending it is a linear patch.

The main `skills/` package is distributed under the upstream MIT license, reproduced in `LICENSE-MIT`. The bundled `CTF-Sandbox-Orchestrator` package is distributed under GPL-3.0; its license is preserved at `skills/LICENSE`. The plugin manifest therefore uses the SPDX expression `MIT AND GPL-3.0-only`.

## Codex compatibility adjustments

- Added `reverse-skill-router` as the discoverable adapter for the upstream root router.
- Added or localized `agents/openai.yaml` display fields without changing the core trigger descriptions in valid upstream `SKILL.md` files.
- Added the required frontmatter to `reverse-engineering/dsl-vm-reverse/SKILL.md`, whose upstream file had no frontmatter and could not be discovered as a Codex skill.
- Replaced the upstream authorization-precedent text that attempted to override AI safety review with an explicit scope and authorization gate. Related wording in the precedent and routing documents was aligned with that gate.
- Added output-path guards to the Bash and PowerShell APK decode helpers so caller-provided task names cannot make `--clean` remove a filesystem root or a path outside the task directory.
- Preserved the remaining upstream skill directories, references, scripts, prompts, default prompts, and implicit-invocation policies.
