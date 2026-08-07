# Oh-my-mermaid upstream provenance

- Source: `https://github.com/oh-my-mermaid/oh-my-mermaid`
- Imported commit: `38ccdb69298adec949177c92c88d6e3ddfb5bab7`
- Upstream manifest version: `0.2.0`
- Imported on: `2026-08-07`
- Imported skills: `omm-scan`, `omm-view`, `omm-push`
- Deprecated skills skipped: 0

The upstream `.claude-plugin/plugin.json` does not declare an explicit skill list, so the import boundary is the three `skills/*/SKILL.md` directories present at the recorded commit. Their `SKILL.md` files are preserved unchanged. Codex-facing Chinese display metadata is supplied separately through each skill's `agents/openai.yaml`.

The skills require the separately installed `oh-my-mermaid` CLI (Node.js 18 or newer). This plugin does not bundle the CLI, credentials, user architecture documents, or cloud data. `omm-push` can upload the current project's `.omm/` directory to `ohmymermaid.com` only when invoked after installation, login, project linking, and the applicable user authorization.
