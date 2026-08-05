# Upstream provenance

- Repository: <https://github.com/DannyMac180/sol-advisor>
- Imported commit: `154fd7ac282088f58246e192347960ba0bfc945f`
- Imported on: 2026-08-05
- Upstream plugin version: `0.4.0`
- Imported skills: 1
- Deprecated skills skipped: 0
- License: MIT

The upstream plugin, native custom-agent templates, scripts, skill, references, README, and license are preserved as one standalone package because their relative paths and verification contracts form a single installation unit.

## Codex marketplace packaging adjustments

- Added `assets/icon.svg` and referenced it from `interface.logo` and `interface.composerIcon`.
- Classified the plugin interface under `AI & Agent`; the marketplace entry keeps this repository's standard `Productivity` category.
- Localized only the user-facing `display_name` and `short_description` in `skills/orchestration/agents/openai.yaml`; the upstream `SKILL.md` trigger contract remains unchanged.
- Made the bundled verifier read the preserved plugin-local upstream README instead of the target marketplace repository README.
- Made the bundled verifier check the retained explicit-authorization wording in `default_prompt` instead of hard-coding the upstream English short description, so Chinese display localization does not weaken or falsely fail the Luna opt-in gate.
- Restored the truthful `Codex app task tools` wording in `interface.longDescription` so the upstream verifier remains aligned after the upstream Luna default-prompt length fix.
