# CTZ Codex Plugins

This repository contains Codex plugins packaged for installation through the Codex App plugin marketplace flow.

## Plugins

- `alibaba-operations-framework`: 1688 operations framework for store diagnosis, product expression, inquiry conversion, paid traffic decisions, fulfillment service, distribution/cross-border supply, and platform risk control.
- `1688-title-optimizer`: 1688 title optimization expert for keyword structure, title rewriting, fact consistency, and compliance risk checks.
- `1688-detail-copywriter`: 1688 detail page copywriting expert for B2B purchasing modules, product facts, service promises, and conversion risk checks.
- `baoyu-skills`: JimLiu/baoyu-skills packaged as a Codex plugin with 20 non-deprecated upstream skills for content generation, image/diagram workflows, markdown/HTML conversion, translation, social publishing, URL extraction, WeChat summaries, and YouTube transcripts.
- `huashu`: alchaincyf/nuwa-skill, alchaincyf/darwin-skill, and alchaincyf/huashu-design packaged as a Codex plugin with `huashu-nuwa` for distilling public figures or themes into runnable perspective skills, `darwin-skill` for evaluating and optimizing Agent Skills, and `huashu-design` for high-fidelity HTML prototypes, demos, slides, animations, and design reviews.
- `xhs-skills`: white0dew/XiaohongshuSkills packaged as a Codex plugin with `RedBookSkills` for Xiaohongshu publishing, login checks, note search, comments, interactions, profile snapshots, and content data export.
- `weread-skills`: WeRead official skills zip packaged as a Codex plugin for book search, bookshelf lookup, notes and highlights, book reviews, reading statistics, recommendations, reading blind-spot analysis, and thinking-structure analysis through `WEREAD_API_KEY`.
- `skill-repo-to-codex-plugin`: reusable workflow for packaging an upstream GitHub skill repository into this Codex plugin marketplace.
- `mattpocock-skills`: Matt Pocock's engineering skills packaged as a Codex plugin with 14 non-deprecated upstream skills for diagnosis, TDD, architecture review, PRDs, issue triage, prototypes, handoffs, and concise communication.

## Install

Add this marketplace in Codex:

```bash
codex plugin marketplace add tianzecn/ctz-codex-plugins
```
