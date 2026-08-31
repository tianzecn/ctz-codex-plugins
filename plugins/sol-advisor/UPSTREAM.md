# Upstream provenance

- Repository: <https://github.com/DannyMac180/sol-advisor>
- Imported commit: `37b75cad535abdd46531f0227483a8842d045ab8`
- Imported on: 2026-08-31
- Upstream plugin version: `0.6.0`
- Imported skills: 1
- Deprecated skills skipped: 0
- License: MIT

The upstream plugin, three native custom-agent templates, scripts, skill, references, README, and license are preserved as one standalone package because their relative paths and verification contracts form a single installation unit.

## Codex marketplace packaging adjustments

- Added `assets/icon.svg` and referenced it from `interface.logo` and `interface.composerIcon`.
- Classified the plugin interface under `AI & Agent`; the marketplace entry keeps this repository's standard `Productivity` category.
- Localized only the user-facing `display_name` and `short_description` in `skills/orchestration/agents/openai.yaml`; the upstream `SKILL.md` trigger contract remains unchanged.
- Made the bundled verifier read the preserved plugin-local upstream README instead of the target marketplace repository README.
- Preserved the upstream selective-routing manifest language and added only the target repository URL, marketplace category, brand color, and icon paths.
