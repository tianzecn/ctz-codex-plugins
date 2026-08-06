# Upstream provenance

- Source: `https://github.com/Fokkyp/SoftwareCopyright-Skill`
- Imported commit: `dfc15dca6555b74c8e0da28963c125d6a1e8e001`
- Imported tag: `v1.3`
- Upstream plugin manifest version: `1.0.0`
- Upstream skill metadata version: `1.3`
- Imported on: `2026-08-07`
- Imported skills: 1
- Deprecated skills skipped: 0
- License: MIT

The import contains the 93 files under the upstream `software-copyright-materials/` directory. The repository-level screenshots, generated demo materials, and the `skills/software-copyright-materials` symlink are outside the declared skill boundary and were not imported. The repository-level MIT license is preserved as `LICENSE`; the vendored DocxToolkit MIT license remains at its upstream path.

Codex-facing adaptations are limited to replacing the Claude-specific skill path placeholder with `{baseDir}`, converting `agents/openai.yaml` to the Codex interface shape, adding explicit project-data and installation approval gates, and keeping environment checks from implicitly running NuGet restore/build. The upstream setup scripts remain otherwise unchanged and were not executed during import.
