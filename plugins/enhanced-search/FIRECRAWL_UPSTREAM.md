# Firecrawl Developer Index upstream provenance

- Distribution source: `https://github.com/firecrawl/skills`
- Imported distribution commit: `8b18f3b161ff3081e8dc8417dcdc8cb24aa0fd9e`
- Canonical source: `https://github.com/firecrawl/cli`
- Canonical source commit: `026c820bebd7040720079a05d4d428c193e23a7b`
- Imported on: `2026-08-22`
- Imported skills: `firecrawl-developer-index`
- Deprecated skills skipped: 0
- Upstream license: ISC

The imported `SKILL.md` from the distribution repository is byte-for-byte identical to the canonical CLI source at the commits recorded above before the Codex compatibility note is applied. Its frontmatter and core workflow remain unchanged. The local compatibility note documents two runtime facts verified during import: this plugin does not bundle Firecrawl CLI or MCP, and Firecrawl may require `FIRECRAWL_API_KEY` when anonymous requests are rejected by IP risk controls.

The API key is a runtime secret. This plugin does not include credentials, request that users paste credentials into chat, or write credentials into the repository.
