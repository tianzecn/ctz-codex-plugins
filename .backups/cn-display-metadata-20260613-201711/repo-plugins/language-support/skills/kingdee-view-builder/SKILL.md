---
name: kingdee-view-builder
description: Build, repair, and explain Kingdee / 金蝶 MSSQL business views in the kingdee workspace. Use when the user asks to create an A_ view, make a report view, inspect or fix SQL Server view binding errors, or turn Kingdee inventory/sales/order requirements, screenshots, Excel references, or SQL drafts into a validated MSSQL view.
metadata:
  short-description: Build Kingdee MSSQL report views
---

# Kingdee View Builder

Use this skill inside `/Users/office/我的云端硬盘/codex/kingdee` for Kingdee / 金蝶 MSSQL view work.

## Core Rules

- This is a Kingdee MSSQL business-view workflow, not a general SQL Server generator.
- New business views must be named `dbo.A_*`. If the user gives a non-`A_` name, normalize it and show the final name before execution.
- Use `CREATE OR ALTER VIEW` by default. Do not use `DROP`.
- Do not add `WITH SCHEMABINDING` by default.
- Use Chinese business column aliases unless the user explicitly asks otherwise.
- Never store or print real credentials. Show only the database name and a masked host in reports.
- Use read-only discovery first. DDL requires explicit user confirmation after showing the summary.
- Do not execute `UPDATE`, `DELETE`, `MERGE`, `TRUNCATE`, `DROP`, `ALTER TABLE`, permission changes, bulk import, or production API calls.
- Do not use `NOLOCK` as a default.

## Configuration

Read connection settings with `scripts/view_tool.py`. Supported variables:

- `KINGDEE_MSSQL_HOST`
- `KINGDEE_MSSQL_PORT`
- `KINGDEE_MSSQL_USER`
- `KINGDEE_MSSQL_PASSWORD`
- `KINGDEE_MSSQL_DATABASE`
- `KINGDEE_MSSQL_CHARSET`
- `KINGDEE_MSSQL_LOGIN_TIMEOUT`
- `KINGDEE_MSSQL_QUERY_TIMEOUT`
- `KINGDEE_DATA_MODEL_PATH`
- Optional: `KINGDEE_WORKSPACE_ROOT`
- Optional: `KINGDEE_VIEW_ENV_FILE`

Resolution order is: process environment > `KINGDEE_VIEW_ENV_FILE` > `~/.codex/secrets/kingdee/.env` > workspace `.env`.
The workspace `.env.example` is only a placeholder. Prefer real secrets in shell environment variables or `~/.codex/secrets/kingdee/.env`.
When installed as a plugin, set `KINGDEE_WORKSPACE_ROOT` or run the tool from the Kingdee workspace so it can find `数据模型/数据模型.html`.

`pymssql` must already be installed in the Python environment being used. If it is missing, report the install command; do not install it automatically.

## Workflow

1. **Understand the request**
   - Accept natural language, screenshots, Excel references, and existing SQL.
   - Identify desired columns, filters, grouping, sorting, view name, and target totals.
   - If a business term has multiple plausible meanings, discover candidates first; ask only about high-impact ambiguities.

2. **Discover before writing SQL**
   - Search `数据模型/数据模型.html` with UTF-16LE-safe commands for business objects.
   - Use live schema queries against `sys.objects`, `sys.columns`, `sys.sql_modules`, `INFORMATION_SCHEMA`, and small samples.
   - Use `scripts/view_tool.py catalog --terms ...` and `view-info` for catalog checks.
   - Default sample size is `TOP 20`; avoid broad table scans.

3. **Build the view contract**
   - Enforce `dbo.A_*`.
   - Prefer direct, explicit joins with two-part object names.
   - Allow dependencies on existing `A_` views only after confirming the upstream view exists and can be selected.
   - Keep zero values only when the request asks for complete data; for report-like screenshots, zero-value groups may be excluded if reported.
   - Preserve and report negative quantities, NULLs, and empty auxiliary attributes rather than silently filtering them.

4. **Before DDL**
   - Save the proposed SQL script in the workspace root as `create_<view_name_lower>_view.sql`.
   - Show the masked target, final view name, output columns, dependencies, whether an old view exists, key SQL summary, and validation plan.
   - Ask for explicit confirmation before running `CREATE OR ALTER VIEW`.

5. **Execute and verify**
   - Execute only through `scripts/view_tool.py execute-view-script --file ... --expected-view dbo.A_X`.
   - Validate with `scripts/view_tool.py validate --view dbo.A_X --sample 20 --auto-sum`.
   - Final report includes script path, columns, sample preview, `COUNT`, automatic `SUM` results, exceptions/anomalies, and a copyable `SELECT`.

## References

- Read `references/kingdee-patterns.md` for known Kingdee table/view mappings.
- Use `examples/` for prompt patterns that should trigger this skill.
