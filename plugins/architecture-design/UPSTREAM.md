# Upstream provenance

## Archify

- Repository: https://github.com/tt-a1i/archify
- Branch: `main`
- Commit: `95e8a3a9d50136bc34e1093edbca7d4a52e974aa`
- Package version: `2.15.0`
- Retrieved: 2026-08-25
- License: MIT; the upstream license is preserved in `skills/archify/LICENSE`.
- Release archive SHA-256: `0df161dd0d780ed240b2d2e1f1eda8c6bb4394253af0ce956d89959487c37e10`

The imported files are the exact contents of the upstream `archify.zip` release package. The
archive was rebuilt from the fixed commit, its extracted tree matched the committed archive, and
the upstream `scripts/package-smoke.mjs` acceptance suite passed on macOS. Repository-only tests,
dependency lockfiles, generators, and development dependencies are intentionally excluded by the
upstream release contract.

Codex-specific packaging adds only `skills/archify/agents/openai.yaml` for bilingual display
metadata. The upstream `SKILL.md`, CLI, renderers, schemas, examples, references, assets, and MIT
license remain unchanged.

## Existing skill

`native-feel-cross-platform-desktop` predates this import and is not modified by the Archify
conversion.
