#!/usr/bin/env python3
"""Utilities for Kingdee MSSQL view discovery, validation, and guarded DDL."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable


SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_SECRET_ENV = Path.home() / ".codex" / "secrets" / "kingdee" / ".env"

REQUIRED_KEYS = (
    "KINGDEE_MSSQL_HOST",
    "KINGDEE_MSSQL_USER",
    "KINGDEE_MSSQL_PASSWORD",
    "KINGDEE_MSSQL_DATABASE",
)

DEFAULTS = {
    "KINGDEE_MSSQL_PORT": "1433",
    "KINGDEE_MSSQL_CHARSET": "UTF-8",
    "KINGDEE_MSSQL_LOGIN_TIMEOUT": "10",
    "KINGDEE_MSSQL_QUERY_TIMEOUT": "30",
    "KINGDEE_DATA_MODEL_PATH": "数据模型/数据模型.html",
}

NUMERIC_TYPES = {
    "bigint",
    "decimal",
    "float",
    "int",
    "money",
    "numeric",
    "real",
    "smallint",
    "smallmoney",
    "tinyint",
}

AUTO_SUM_PATTERNS = (
    "数量",
    "库存",
    "金额",
    "价税",
    "未出",
    "出库",
    "余额",
    "qty",
    "quantity",
    "amount",
    "stock",
    "balance",
)

DANGEROUS_SQL_PATTERNS = (
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bMERGE\b",
    r"\bTRUNCATE\b",
    r"\bDROP\b",
    r"\bINSERT\b",
    r"\bALTER\s+(?!VIEW\b)",
    r"\bCREATE\s+(?!OR\s+ALTER\s+VIEW\b)(?!VIEW\b)",
    r"\bGRANT\b",
    r"\bDENY\b",
    r"\bREVOKE\b",
    r"\bBACKUP\b",
    r"\bRESTORE\b",
    r"\bBULK\b",
    r"\bOPENROWSET\b",
    r"\bOPENDATASOURCE\b",
    r"\bXP_",
    r"\bSP_CONFIGURE\b",
)


class ToolError(RuntimeError):
    """User-facing tool error."""


@dataclass(frozen=True)
class Config:
    values: dict[str, str]
    sources: dict[str, str]

    @property
    def host(self) -> str:
        return self.values["KINGDEE_MSSQL_HOST"]

    @property
    def masked_host(self) -> str:
        host = self.host
        if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
            parts = host.split(".")
            return f"{parts[0]}.{parts[1]}.***.***"
        if len(host) <= 6:
            return "***"
        return f"{host[:3]}***{host[-3:]}"

    @property
    def database(self) -> str:
        return self.values["KINGDEE_MSSQL_DATABASE"]

    def public_dict(self) -> dict[str, Any]:
        env_source = self.sources.get("__env_file__")
        return {
            "host": self.masked_host,
            "port": self.values.get("KINGDEE_MSSQL_PORT"),
            "database": self.database,
            "charset": self.values.get("KINGDEE_MSSQL_CHARSET"),
            "login_timeout": int(self.values.get("KINGDEE_MSSQL_LOGIN_TIMEOUT", "10")),
            "query_timeout": int(self.values.get("KINGDEE_MSSQL_QUERY_TIMEOUT", "30")),
            "data_model_path": self.values.get("KINGDEE_DATA_MODEL_PATH"),
            "workspace_root": self.values.get("KINGDEE_WORKSPACE_ROOT"),
            "env_file_used": str(env_source) if env_source else None,
            "workspace_env_warning": bool(env_source)
            and self.values.get("KINGDEE_WORKSPACE_ROOT")
            and env_source == str(Path(self.values["KINGDEE_WORKSPACE_ROOT"]) / ".env"),
        }


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value
    return values


def load_config() -> Config:
    values = dict(DEFAULTS)
    sources: dict[str, str] = {key: "default" for key in DEFAULTS}

    workspace_root = resolve_workspace_root()
    if workspace_root:
        values["KINGDEE_WORKSPACE_ROOT"] = str(workspace_root)
        sources["KINGDEE_WORKSPACE_ROOT"] = "auto-detected"

    candidate_files: list[Path] = []
    if workspace_root and (workspace_root / ".env").exists():
        candidate_files.append(workspace_root / ".env")
    if DEFAULT_SECRET_ENV.exists():
        candidate_files.append(DEFAULT_SECRET_ENV)
    explicit_env_file = os.environ.get("KINGDEE_VIEW_ENV_FILE")
    if explicit_env_file:
        candidate_files.append(Path(explicit_env_file).expanduser())

    for env_file in candidate_files:
        parsed = parse_env_file(env_file)
        if parsed:
            sources["__env_file__"] = str(env_file)
        for key, value in parsed.items():
            if key.startswith("KINGDEE_"):
                values[key] = value
                sources[key] = str(env_file)

    for key, value in os.environ.items():
        if key.startswith("KINGDEE_"):
            values[key] = value
            sources[key] = "process environment"

    missing = [key for key in REQUIRED_KEYS if not values.get(key)]
    if missing:
        raise ToolError(
            "Missing required configuration variables: "
            + ", ".join(missing)
            + ". Set them in the environment or a local-only env file."
        )

    return Config(values=values, sources=sources)


def resolve_workspace_root() -> Path | None:
    explicit_root = os.environ.get("KINGDEE_WORKSPACE_ROOT")
    if explicit_root:
        return Path(explicit_root).expanduser().resolve()

    start_points = [Path.cwd().resolve()]
    for start in start_points:
        for candidate in (start, *start.parents):
            if (candidate / "数据模型" / "数据模型.html").exists():
                return candidate
            if (candidate / ".env.example").exists() and candidate.name == "kingdee":
                return candidate
    return None


def require_pymssql():
    try:
        import pymssql  # type: ignore
    except ModuleNotFoundError as exc:
        raise ToolError(
            "Python package 'pymssql' is not installed. Install it in the Python "
            "environment you use to run this script, for example: python3 -m pip install pymssql"
        ) from exc
    return pymssql


def connect(config: Config):
    pymssql = require_pymssql()
    return pymssql.connect(
        server=config.values["KINGDEE_MSSQL_HOST"],
        port=int(config.values.get("KINGDEE_MSSQL_PORT", "1433")),
        user=config.values["KINGDEE_MSSQL_USER"],
        password=config.values["KINGDEE_MSSQL_PASSWORD"],
        database=config.values["KINGDEE_MSSQL_DATABASE"],
        charset=config.values.get("KINGDEE_MSSQL_CHARSET", "UTF-8"),
        login_timeout=int(config.values.get("KINGDEE_MSSQL_LOGIN_TIMEOUT", "10")),
        timeout=int(config.values.get("KINGDEE_MSSQL_QUERY_TIMEOUT", "30")),
    )


def json_default(value: Any) -> Any:
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    if hasattr(value, "isoformat"):
        return value.isoformat(sep=" ")  # datetime/date
    return str(value)


def print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=json_default))


def parse_view_name(view: str) -> tuple[str, str]:
    normalized = view.strip().replace("[", "").replace("]", "").replace('"', "")
    if "." in normalized:
        schema, name = normalized.split(".", 1)
    else:
        schema, name = "dbo", normalized
    schema = schema.strip() or "dbo"
    name = name.strip()
    if not name:
        raise ToolError("View name is empty.")
    if not name.upper().startswith("A_"):
        raise ToolError(f"Expected an A_ view name, got {schema}.{name}.")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", schema):
        raise ToolError(f"Unsafe schema name: {schema}")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise ToolError(f"Unsafe view name: {name}")
    return schema, name


def bracket(identifier: str) -> str:
    return "[" + identifier.replace("]", "]]") + "]"


def object_literal(schema: str, name: str) -> str:
    return f"{bracket(schema)}.{bracket(name)}"


def object_name_param(schema: str, name: str) -> str:
    return f"{schema}.{name}"


def fetchall(cursor) -> list[dict[str, Any]]:
    return list(cursor.fetchall())


def command_check_config(args: argparse.Namespace) -> None:
    config = load_config()
    payload: dict[str, Any] = {
        "ok": True,
        "target": config.public_dict(),
        "pymssql": "available",
    }
    require_pymssql()
    if not args.no_connect:
        with connect(config) as conn:
            cursor = conn.cursor(as_dict=True)
            cursor.execute("SELECT DB_NAME() AS database_name")
            payload["connection"] = fetchall(cursor)[0]
    print_json(payload)


def command_catalog(args: argparse.Namespace) -> None:
    terms = [term.strip() for term in args.terms if term.strip()]
    if not terms:
        raise ToolError("catalog requires at least one --terms value.")
    limit = max(1, min(args.limit, 500))
    config = load_config()
    patterns = [f"%{term}%" for term in terms]

    with connect(config) as conn:
        cursor = conn.cursor(as_dict=True)
        object_rows: list[dict[str, Any]] = []
        column_rows: list[dict[str, Any]] = []
        module_rows: list[dict[str, Any]] = []

        for pattern in patterns:
            cursor.execute(
                f"""
                SELECT TOP {limit}
                    s.name AS schema_name,
                    o.name AS object_name,
                    o.type_desc
                FROM sys.objects AS o
                INNER JOIN sys.schemas AS s ON s.schema_id = o.schema_id
                WHERE o.name LIKE %s
                  AND o.type IN ('U', 'V', 'P', 'IF', 'TF', 'FN')
                ORDER BY o.name;
                """,
                (pattern,),
            )
            object_rows.extend(fetchall(cursor))

            cursor.execute(
                f"""
                SELECT TOP {limit}
                    s.name AS schema_name,
                    o.name AS object_name,
                    o.type_desc,
                    c.name AS column_name,
                    t.name AS type_name,
                    c.column_id
                FROM sys.columns AS c
                INNER JOIN sys.objects AS o ON o.object_id = c.object_id
                INNER JOIN sys.schemas AS s ON s.schema_id = o.schema_id
                INNER JOIN sys.types AS t ON t.user_type_id = c.user_type_id
                WHERE c.name LIKE %s
                  AND o.type IN ('U', 'V')
                ORDER BY o.name, c.column_id;
                """,
                (pattern,),
            )
            column_rows.extend(fetchall(cursor))

            cursor.execute(
                f"""
                SELECT TOP {limit}
                    s.name AS schema_name,
                    o.name AS object_name,
                    o.type_desc,
                    LEFT(m.definition, 600) AS definition_preview
                FROM sys.sql_modules AS m
                INNER JOIN sys.objects AS o ON o.object_id = m.object_id
                INNER JOIN sys.schemas AS s ON s.schema_id = o.schema_id
                WHERE m.definition LIKE %s
                ORDER BY o.name;
                """,
                (pattern,),
            )
            module_rows.extend(fetchall(cursor))

    print_json(
        {
            "target": config.public_dict(),
            "terms": terms,
            "objects": dedupe_rows(object_rows),
            "columns": dedupe_rows(column_rows),
            "modules": dedupe_rows(module_rows),
        }
    )


def dedupe_rows(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for row in rows:
        key = json.dumps(row, sort_keys=True, default=json_default)
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result


def command_view_info(args: argparse.Namespace) -> None:
    schema, name = parse_view_name(args.view)
    config = load_config()
    with connect(config) as conn:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(
            """
            SELECT
                s.name AS schema_name,
                o.name AS object_name,
                o.type_desc,
                o.create_date,
                o.modify_date,
                m.definition
            FROM sys.objects AS o
            INNER JOIN sys.schemas AS s ON s.schema_id = o.schema_id
            LEFT JOIN sys.sql_modules AS m ON m.object_id = o.object_id
            WHERE s.name = %s AND o.name = %s;
            """,
            (schema, name),
        )
        objects = fetchall(cursor)

        columns: list[dict[str, Any]] = []
        dependencies: list[dict[str, Any]] = []
        can_select = False
        select_error = None
        if objects:
            cursor.execute(
                """
                SELECT
                    c.column_id,
                    c.name AS column_name,
                    t.name AS type_name,
                    c.max_length,
                    c.precision,
                    c.scale,
                    c.is_nullable
                FROM sys.columns AS c
                INNER JOIN sys.types AS t ON t.user_type_id = c.user_type_id
                WHERE c.object_id = OBJECT_ID(%s)
                ORDER BY c.column_id;
                """,
                (object_name_param(schema, name),),
            )
            columns = fetchall(cursor)

            cursor.execute(
                """
                SELECT
                    referenced_schema_name,
                    referenced_entity_name,
                    referenced_minor_name,
                    is_ambiguous
                FROM sys.sql_expression_dependencies
                WHERE referencing_id = OBJECT_ID(%s)
                ORDER BY referenced_schema_name, referenced_entity_name, referenced_minor_name;
                """,
                (object_name_param(schema, name),),
            )
            dependencies = fetchall(cursor)

            try:
                cursor.execute(f"SELECT TOP 1 * FROM {object_literal(schema, name)}")
                cursor.fetchall()
                can_select = True
            except Exception as exc:  # noqa: BLE001 - report DB driver message
                select_error = str(exc)

    print_json(
        {
            "target": config.public_dict(),
            "view": object_name_param(schema, name),
            "exists": bool(objects),
            "object": objects[0] if objects else None,
            "columns": columns,
            "dependencies": dependencies,
            "can_select": can_select,
            "select_error": select_error,
        }
    )


def command_validate(args: argparse.Namespace) -> None:
    schema, name = parse_view_name(args.view)
    sample_size = max(1, min(args.sample, 200))
    config = load_config()
    object_ref = object_literal(schema, name)
    with connect(config) as conn:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(
            """
            SELECT
                c.column_id,
                c.name AS column_name,
                t.name AS type_name,
                c.max_length,
                c.precision,
                c.scale,
                c.is_nullable
            FROM sys.columns AS c
            INNER JOIN sys.types AS t ON t.user_type_id = c.user_type_id
            WHERE c.object_id = OBJECT_ID(%s)
            ORDER BY c.column_id;
            """,
            (object_name_param(schema, name),),
        )
        columns = fetchall(cursor)
        if not columns:
            raise ToolError(f"View does not exist or has no columns: {schema}.{name}")

        cursor.execute(f"SELECT COUNT_BIG(*) AS row_count FROM {object_ref};")
        count_row = fetchall(cursor)[0]

        sum_rows: list[dict[str, Any]] = []
        if args.auto_sum:
            sum_columns = auto_sum_columns(columns)
            if sum_columns:
                expressions = [
                    f"SUM(COALESCE(CAST({bracket(col['column_name'])} AS decimal(38, 6)), 0)) AS {bracket(col['column_name'])}"
                    for col in sum_columns
                ]
                cursor.execute(f"SELECT {', '.join(expressions)} FROM {object_ref};")
                sum_rows = fetchall(cursor)

        cursor.execute(f"SELECT TOP {sample_size} * FROM {object_ref};")
        sample_rows = fetchall(cursor)

    print_json(
        {
            "target": config.public_dict(),
            "view": object_name_param(schema, name),
            "columns": columns,
            "count": count_row,
            "auto_sum": sum_rows[0] if sum_rows else {},
            "sample": sample_rows,
        }
    )


def auto_sum_columns(columns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for col in columns:
        type_name = str(col["type_name"]).lower()
        column_name = str(col["column_name"]).lower()
        if type_name not in NUMERIC_TYPES:
            continue
        if any(pattern.lower() in column_name for pattern in AUTO_SUM_PATTERNS):
            result.append(col)
    return result


def command_execute_view_script(args: argparse.Namespace) -> None:
    schema, name = parse_view_name(args.expected_view)
    script_path = Path(args.file).expanduser().resolve()
    if not script_path.exists():
        raise ToolError(f"Script file does not exist: {script_path}")
    if not script_path.is_file():
        raise ToolError(f"Script path is not a file: {script_path}")

    sql = script_path.read_text(encoding="utf-8")
    validate_view_script(sql, schema, name)
    batches = split_batches(sql)
    if not batches:
        raise ToolError("Script has no executable SQL batches.")

    config = load_config()
    with connect(config) as conn:
        cursor = conn.cursor(as_dict=True)
        for batch in batches:
            cursor.execute(batch)
        conn.commit()
        cursor.execute(
            """
            SELECT
                s.name AS schema_name,
                o.name AS object_name,
                o.type_desc,
                o.modify_date
            FROM sys.objects AS o
            INNER JOIN sys.schemas AS s ON s.schema_id = o.schema_id
            WHERE s.name = %s AND o.name = %s AND o.type = 'V';
            """,
            (schema, name),
        )
        rows = fetchall(cursor)
        if not rows:
            raise ToolError(f"Expected view was not found after execution: {schema}.{name}")

    print_json(
        {
            "ok": True,
            "target": config.public_dict(),
            "script": str(script_path),
            "view": object_name_param(schema, name),
            "object": rows[0],
        }
    )


def split_batches(sql: str) -> list[str]:
    batches: list[str] = []
    current: list[str] = []
    for line in sql.splitlines():
        if re.fullmatch(r"\s*GO\s*(?:--.*)?", line, flags=re.IGNORECASE):
            batch = "\n".join(current).strip()
            if batch:
                batches.append(batch)
            current = []
        else:
            current.append(line)
    tail = "\n".join(current).strip()
    if tail:
        batches.append(tail)
    return batches


def strip_comments_and_literals(sql: str) -> str:
    output: list[str] = []
    i = 0
    length = len(sql)
    state = "normal"
    while i < length:
        ch = sql[i]
        nxt = sql[i + 1] if i + 1 < length else ""
        if state == "normal":
            if ch == "-" and nxt == "-":
                state = "line_comment"
                output.append(" ")
                i += 2
                continue
            if ch == "/" and nxt == "*":
                state = "block_comment"
                output.append(" ")
                i += 2
                continue
            if ch in ("'", '"'):
                quote = ch
                state = f"string:{quote}"
                output.append(" ")
                i += 1
                continue
            output.append(ch)
            i += 1
            continue
        if state == "line_comment":
            if ch == "\n":
                output.append("\n")
                state = "normal"
            i += 1
            continue
        if state == "block_comment":
            if ch == "*" and nxt == "/":
                state = "normal"
                i += 2
            else:
                i += 1
            continue
        if state.startswith("string:"):
            quote = state.split(":", 1)[1]
            if ch == quote:
                if nxt == quote:
                    i += 2
                else:
                    state = "normal"
                    i += 1
            else:
                i += 1
            continue
    return "".join(output)


def validate_view_script(sql: str, schema: str, name: str) -> None:
    stripped = strip_comments_and_literals(sql)
    normalized = re.sub(r"\s+", " ", stripped).strip()
    upper = normalized.upper()

    for pattern in DANGEROUS_SQL_PATTERNS:
        if re.search(pattern, upper, flags=re.IGNORECASE):
            raise ToolError(f"Refusing unsafe SQL pattern: {pattern}")

    view_pattern = re.compile(
        r"\bCREATE\s+OR\s+ALTER\s+VIEW\s+"
        + r"(?:\[" + re.escape(schema) + r"\]|" + re.escape(schema) + r")"
        + r"\s*\.\s*"
        + r"(?:\[" + re.escape(name) + r"\]|" + re.escape(name) + r")\b",
        flags=re.IGNORECASE,
    )
    if not view_pattern.search(normalized):
        raise ToolError(f"Script must contain CREATE OR ALTER VIEW {schema}.{name}.")

    if not re.search(r"\bAS\s+(SELECT|WITH)\b", upper, flags=re.IGNORECASE):
        raise ToolError("Script must contain AS SELECT or AS WITH for the view definition.")

    disallowed_exec = re.search(r"\bEXEC(?:UTE)?\b", upper, flags=re.IGNORECASE)
    if disallowed_exec:
        raise ToolError("EXEC/EXECUTE is not allowed in view scripts.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_config = subparsers.add_parser("check-config", help="Validate config and pymssql.")
    check_config.add_argument("--no-connect", action="store_true", help="Skip DB connection test.")
    check_config.set_defaults(func=command_check_config)

    catalog = subparsers.add_parser("catalog", help="Search objects, columns, and module definitions.")
    catalog.add_argument("--terms", nargs="+", required=True, help="Search terms.")
    catalog.add_argument("--limit", type=int, default=100, help="Max rows per term per section.")
    catalog.set_defaults(func=command_catalog)

    view_info = subparsers.add_parser("view-info", help="Inspect an A_ view.")
    view_info.add_argument("--view", required=True, help="Two-part view name, e.g. dbo.A_STK_INVENTORY.")
    view_info.set_defaults(func=command_view_info)

    validate = subparsers.add_parser("validate", help="Validate an A_ view.")
    validate.add_argument("--view", required=True, help="Two-part view name, e.g. dbo.A_STK_INVENTORY.")
    validate.add_argument("--sample", type=int, default=20, help="Number of sample rows.")
    validate.add_argument("--auto-sum", action="store_true", help="SUM numeric quantity/amount-like columns.")
    validate.set_defaults(func=command_validate)

    execute = subparsers.add_parser("execute-view-script", help="Execute a guarded CREATE OR ALTER VIEW script.")
    execute.add_argument("--file", required=True, help="SQL script path.")
    execute.add_argument("--expected-view", required=True, help="Expected dbo.A_* view name.")
    execute.set_defaults(func=command_execute_view_script)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except ToolError as exc:
        print_json({"ok": False, "error": str(exc)})
        return 2
    except Exception as exc:  # noqa: BLE001 - keep driver failures visible
        print_json({"ok": False, "error": str(exc), "error_type": type(exc).__name__})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
