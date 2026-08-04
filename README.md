# CTZ Codex Plugins

This repository contains Codex plugins packaged for installation through the Codex App plugin marketplace flow.

## Plugins

- `alibaba-operations-framework`: 1688 operations framework for store diagnosis, product expression, inquiry conversion, paid traffic decisions, fulfillment service, distribution/cross-border supply, and platform risk control.
- `1688-title-optimizer`: 1688 title optimization expert for keyword structure, title rewriting, fact consistency, and compliance risk checks.
- `1688-detail-copywriter`: 1688 detail page copywriting expert for B2B purchasing modules, product facts, service promises, and conversion risk checks.
- `baoyu-skills`: JimLiu/baoyu-skills packaged as a Codex plugin with 20 non-deprecated upstream skills for content generation, image/diagram workflows, markdown/HTML conversion, translation, social publishing, URL extraction, WeChat summaries, and YouTube transcripts.
- `huashu`: alchaincyf/nuwa-skill, alchaincyf/darwin-skill, and alchaincyf/huashu-design packaged as a Codex plugin with `huashu-nuwa` for distilling public figures or themes into runnable perspective skills, `darwin-skill` for evaluating and optimizing Agent Skills, and `huashu-design` for high-fidelity HTML prototypes, demos, slides, animations, and design reviews.
- `xhs-skills`: white0dew/XiaohongshuSkills packaged as a Codex plugin with `RedBookSkills` for Xiaohongshu publishing, login checks, note search, comments, interactions, profile snapshots, and content data export.
- `weread-skills`: WeRead official skills zip plus alchaincyf/huashu-weread and yaojingang/yao-open-skills `yao-weread-skill` packaged as one Codex plugin for book search, bookshelf lookup, notes and highlights, book reviews, reading statistics, recommendations, blind-spot analysis, note alchemy, reading reviews, and visual HTML reading reports through `WEREAD_API_KEY`.
- `skill-repo-to-codex-plugin`: reusable workflow for packaging an upstream GitHub skill repository into this Codex plugin marketplace.
- `wechat-publishing`: limin112/wechat-publish-template packaged as a Codex plugin with `wechat-publish-template` for turning Markdown drafts into inline-style WeChat Official Account HTML using an orange-black personal technical article template.
- `mattpocock-skills`: Matt Pocock's engineering skills packaged as a Codex plugin with 22 upstream-declared skills for grilling, specs and tickets, implementation, diagnosis, TDD, code review, domain modeling, architecture improvement, issue triage, research, prototypes, and handoffs.
- `video-generation`: NarratorAI-Studio/narrator-ai-cli-skill packaged as a Codex plugin with `narrator-ai-cli` for AI movie and short-drama narration video workflows, including built-in materials, BGM, dubbing voices, templates, script generation, clip data, video composing, and optional visual templates.
- `task-planning`: OthmanAdi/planning-with-files packaged as a Codex plugin with the canonical `planning-with-files` skill plus Arabic, German, Spanish, Simplified Chinese, and Traditional Chinese variants for persistent markdown task planning, progress tracking, plan checks, and session recovery.
- `knowledge-base-management`: joeseesun/qiaomu-anything-to-notebooklm and PleasePrompto/notebooklm-skill packaged as a Codex plugin with `qiaomu-anything-to-notebooklm` for sending WeChat articles, web pages, YouTube links, podcasts, PDFs, Office documents, EPUBs, images, audio, and search results to NotebookLM, plus `notebooklm` for querying saved NotebookLM notebooks through local browser automation and returning source-grounded answers.
- `enhanced-search`: anysearch-ai/anysearch-skill packaged as a Codex plugin with `anysearch` for real-time web search, vertical domain search, parallel batch search, and full-page URL content extraction through bundled cross-platform CLI tools.
- `ui-design`: Leonxlnx/taste-skill and JimLiu/baoyu-design packaged as a Codex plugin for premium frontend direction, redesign audits, image-to-code workflows, visual style variants, image-generation prompts, and Claude Design style local HTML mockups, wireframes, interactive prototypes, app screens, landing pages, dashboards, and slide decks.
- `code-analysis`: GitHub/awesome-copilot `project-workflow-analysis-blueprint-generator` packaged as a Codex plugin for analyzing representative end-to-end application workflows and generating implementation-ready blueprints.
- `skill-generation`: LearnPrompt/luban-skill and yaojingang/yao-meta-skill packaged as a Codex plugin for creating, auditing, benchmarking, evaluating, governing, packaging, validating, and publishing reusable Agent Skills.
- `image-generation`: tmchow/illo-skill packaged as a Codex plugin for original editorial illustrations, mascot-led visual metaphors, article art, hand-built explainer diagrams, mini-comics, custom characters, and print-style visual systems.
- `mobile-development`: Dimillian/Skills packaged as a Codex plugin with 16 skills for iOS simulator debugging, macOS app packaging, SwiftUI patterns and performance, Swift concurrency, App Store release notes, GitHub workflows, bug hunts, review swarms, refactors, project skill audits, and React component performance.
- `poster-design`: op7418/guizang-social-card-skill packaged as a Codex plugin for Xiaohongshu/Rednote social card sets, WeChat Official Account 21:9 + 1:1 cover pairs, carousel images, article covers, screenshot-heavy posts, and editorial or Swiss-style poster systems.
- `deep-research`: Imbad0202/academic-research-skills-codex packaged as a Codex plugin with the single `academic-research-suite` skill for deep research, literature reviews, systematic reviews, academic paper drafting and revision, peer review simulation, research-to-paper pipelines, experiment planning, and reproducibility checks.
- `oz-skills`: warpdotdev/oz-skills packaged as a Codex plugin with 15 non-deprecated Agent Skills for docs updates, Terraform style, CI fixes, repository investigation, scheduling, SEO/AEO, accessibility, dbt lookup, PR creation, web app testing, performance audits, analysis artifacts, MCP building, bug triage, and issue dedupe.
- `product-planning`: phuryn/pm-skills packaged as a Codex plugin with 68 PM skills for product discovery, strategy, execution, market research, analytics, GTM, growth, PM utility work, and AI-built software shipping checks.
- `multi-model-collaboration`: a capability plugin combining `gpt56-sol-pro-consult`, `workbuddy-cli-model-bridge`, LearnPrompt/partner-skill, and its standalone `idea-king` companion for verified second-opinion reviews, safe WorkBuddy CLI model registration, bidirectional Claude Code/Codex orchestration, and first-principles adversarial plan review.
- `security-scanning`: zhaoxuya520/reverse-skill packaged as a Codex plugin with 83 routing and specialist entries for reverse engineering, explicitly authorized security testing, malware analysis, forensics, mobile and firmware research, cloud and identity security, threat hunting, and CTF sandboxes, with a Codex-compatible authorization gate.

## Install

Add this marketplace in Codex:

```bash
codex plugin marketplace add tianzecn/ctz-codex-plugins
```
