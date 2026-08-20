# Upstream provenance

- Repository: https://github.com/xapi-labs/xapi-cli
- Commit: `7324b97c14533424c7dbfe55eb132ca938d69949`
- Upstream package version: `0.1.19`
- Imported: 2026-08-20
- Imported skills: 1 (`xapi`)
- Deprecated skills skipped: 0
- License: MIT (see `skills/xapi/LICENSE`)

The plugin imports only the upstream `skills/xapi/` directory. It does not
bundle the xapi-to CLI source, build output, examples, tests, or development
dependencies; runtime commands continue to use the separately published
`xapi-to` npm package through `npx`.

The upstream skill content and bundled script are kept unchanged. The Codex
package adds the upstream MIT license and natural Chinese display metadata in
`skills/xapi/agents/openai.yaml`.

Packaging validation does not register an xAPI account, read credentials, call
external APIs, create billable sandboxes, top up an account, or perform social
write actions.
