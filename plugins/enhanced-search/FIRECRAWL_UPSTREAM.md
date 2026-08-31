# Firecrawl Developer Index upstream provenance

- Distribution source: `https://github.com/firecrawl/skills`
- Imported distribution commit: `f6c9b2dd6384e0f05f713727ed18ba9db94d5191`
- Canonical source: `https://github.com/firecrawl/cli`
- Canonical release: `v1.23.3`
- Canonical source commit: `86aaf06cb139029ff5ad2a249670f42b01d40b13`
- Imported on: `2026-08-22`
- Imported skills: `firecrawl-developer-index`
- Deprecated skills skipped: 0
- Upstream license: ISC

The imported `SKILL.md` from the distribution repository is byte-for-byte identical to the canonical CLI source at the commits recorded above before the Codex compatibility note is applied. Its frontmatter and core workflow remain unchanged. The local compatibility note documents two runtime facts verified during import: this plugin does not bundle Firecrawl CLI or MCP, and Firecrawl may require `FIRECRAWL_API_KEY` when anonymous requests are rejected by IP risk controls.

The API key is a runtime secret. This plugin does not include credentials, request that users paste credentials into chat, or write credentials into the repository.
