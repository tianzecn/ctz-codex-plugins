# Upstream Sources

This capability plugin combines skills from multiple upstream repositories.

## planning-with-files

- Repository: <https://github.com/OthmanAdi/planning-with-files>
- Release: `v3.12.0`
- Upstream commit: `d5d35e6a2316459418e7381faa2682b2894d02c1`
- License: MIT; retained in `LICENSE`
- Local skills: `planning-with-files` plus its Arabic, German, Spanish,
  Simplified Chinese, and Traditional Chinese variants

The canonical skill uses the upstream Codex-specific
`.codex/skills/planning-with-files/` variant. Arabic, German, Spanish, Simplified Chinese, and
Traditional Chinese variants use `skills/i18n/`. Unsupported top-level hook metadata is retained
under the standard `metadata` field; no separate compatibility hook layer is added.

## yskills

- Repository: <https://github.com/lycfyi/yskills>
- Upstream commit: `5d30c889820dfbcbaf6a51b29ee97cdfadfae18f`
- Upstream plugin version at import: `0.1.0`
- License: MIT; retained in `LICENSE-YSKILLS`
- Imported paths: `skills/human-context-rebuild/` and `skills/whats-next/`

The imported skill content is unchanged except for:

- natural Chinese `display_name` and `short_description` values in newly added
  `agents/openai.yaml` files;
- the `whats-next` structured-question step, which uses Codex
  `request_user_input`, its two-to-three-option limit, and separate questions
  instead of Claude's `AskUserQuestion`, four-option allowance, and
  `multiSelect` field.
