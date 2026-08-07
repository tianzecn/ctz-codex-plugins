# Upstream provenance

- Repository: <https://github.com/DietrichGebert/ponytail>
- Imported commit: `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`
- Imported on: 2026-08-07
- Upstream version: `4.8.4`
- Imported skills: 6
- Deprecated skills skipped: 0

The imported skills and logo are distributed under the upstream MIT license, reproduced in `LICENSE-PONYTAIL`.

## Codex compatibility adjustments

- Imported the six skill directories declared by the upstream Codex manifest and omitted unrelated commands, benchmarks, MCP adapters, and host-specific integrations.
- Omitted the upstream `hooks` manifest field and lifecycle hook files because the target marketplace validator does not accept that field. Skills are explicitly invoked instead of automatically activated at session start.
- Removed the unsupported `argument-hint` key from `ponytail` frontmatter; the `lite`, `full`, and `ultra` arguments remain documented in the skill body.
- Updated `ponytail-help` to describe the explicit Codex skill flow and removed configuration and update instructions that depend on the omitted lifecycle hooks.
- Added natural Chinese display metadata under each skill's `agents/openai.yaml` without changing the other four upstream `SKILL.md` files.
