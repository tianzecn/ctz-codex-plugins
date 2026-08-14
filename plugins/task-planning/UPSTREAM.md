# Upstream Sources

This capability plugin combines skills from multiple upstream repositories.

## planning-with-files

- Repository: <https://github.com/OthmanAdi/planning-with-files>
- Target repository import commit: `d7cda62a2ff6ae762dd60a02fdcc339925d628b2`
- License: MIT; retained in `LICENSE`
- Local skills: `planning-with-files` plus its Arabic, German, Spanish,
  Simplified Chinese, and Traditional Chinese variants

The original upstream commit was not recorded when these skills were first
imported. The target repository commit above identifies the exact retained
snapshot.

## yskills

- Repository: <https://github.com/lycfyi/yskills>
- Upstream commit: `fcdd7f7cff6cb7e7aab04dfd6713997a94f83ad1`
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
