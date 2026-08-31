# Upstream provenance

- Repository: https://github.com/JimLiu/baoyu-skills
- Release: `v2.5.2`
- Commit: `f490f7e5e347a356cbce30fee193766b7de792cf`
- Imported: 2026-08-31
- Imported skills: 21
- Deprecated skills skipped: 0
- Marketplace-declared license: MIT

The import follows the 21 skill paths declared by the upstream
`.claude-plugin/marketplace.json`. The release tag does not contain a root LICENSE file; this
target retains its existing MIT license text and does not claim that file was copied from the tag.

Upstream replacements are applied without aliases:

- `baoyu-imagine` is replaced by `baoyu-image-gen`.
- `baoyu-image-cards` is replaced by `baoyu-xhs-images`.

Codex-incompatible frontmatter fields are preserved under `metadata`. Natural Chinese display
metadata is maintained separately in `agents/openai.yaml`.
