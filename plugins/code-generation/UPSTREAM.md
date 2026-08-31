# Upstream provenance

- Repository: <https://github.com/DietrichGebert/ponytail>
- Imported commit: `0a4dd63ad4541f4f655c4108a295916f3c1d8fda`
- Imported on: 2026-08-31
- Upstream version: `4.9.0`
- Imported skills: 6
- Deprecated skills skipped: 0

The imported skills and logo are distributed under the upstream MIT license, reproduced in `LICENSE-PONYTAIL`.

## Codex compatibility adjustments

- Imported the six skill directories declared by the upstream Codex manifest and omitted unrelated commands, benchmarks, MCP adapters, and host-specific integrations.
- Omitted the upstream `hooks` manifest field and lifecycle hook files because the target marketplace validator does not accept that field. Skills are explicitly invoked instead of automatically activated at session start.
- Removed the unsupported `argument-hint` key from `ponytail` frontmatter; the `lite`, `full`, and `ultra` arguments remain documented in the skill body.
- Updated `ponytail-help` to describe the explicit Codex skill flow and removed configuration and update instructions that depend on the omitted lifecycle hooks.
- Added natural Chinese display metadata under each skill's `agents/openai.yaml` without changing the other four upstream `SKILL.md` files.
