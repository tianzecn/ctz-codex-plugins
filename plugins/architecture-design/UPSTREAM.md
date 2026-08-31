# Upstream provenance

## Archify

- Repository: https://github.com/tt-a1i/archify
- Release: `v2.16.0`
- Commit: `c826e6c3a7abad19c0f3cd1ca57207d54b1ad8de`
- Package version: `2.16.0`
- Retrieved: 2026-08-31
- License: MIT; the upstream license is preserved in `skills/archify/LICENSE`.
- Release archive SHA-256: `4c59fa6557a2385beaaef8c7219cc414573acc9f0c30a932d5053b0b20689a46`

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
