# Kingdee View Patterns

This reference captures verified Kingdee / 金蝶 MSSQL patterns for this workspace. Recheck live schema before executing SQL.

## Discovery Anchors

- Data model export: `数据模型/数据模型.html`, UTF-16LE.
- Search safely:
  - `rg --encoding utf-16le "销售订单|即时库存|客户|物料|表名称" "数据模型/数据模型.html"`
  - `iconv -f UTF-16LE -t UTF-8 "数据模型/数据模型.html" | sed -n '1,80p'`
- Always validate object names and columns through `sys.objects`, `sys.columns`, `sys.sql_modules`, or `INFORMATION_SCHEMA`.

## View Naming

- Business/report views created by this workflow use `dbo.A_*`.
- Root-level SQL scripts should be named `create_<view_name_lower>_view.sql`.
- Existing workspace examples include sales progress and sales-not-out scripts.

## Sales Order Progress

Common sources:

- `dbo.T_SAL_ORDER` as sales order header.
- `dbo.T_SAL_ORDERENTRY` as sales order entry.
- `dbo.T_SAL_ORDERENTRY_F` for price/amount fields.
- `dbo.T_SAL_ORDERENTRY_R` for stock-out progress fields.
- Customer names through `dbo.T_BD_CUSTOMER_L` with `FLOCALEID = 2052`.
- Material names through `dbo.T_BD_MATERIAL` and `dbo.T_BD_MATERIAL_L`.
- Unit names through `dbo.T_BD_UNIT_L`.
- Auxiliary attribute display values through `dbo.T_BD_FLEXSITEMDETAILV` and auxiliary data entry language tables.

Common filters:

- Latest valid sales order version: `T_SAL_ORDER.FFINALVERSION = '1'`.
- Not cancelled: `T_SAL_ORDER.FCANCELSTATUS = 'A'`.
- Unshipped order lines: remaining outbound quantity > 0.

## Instant Inventory

Verified model anchors:

- `dbo.T_STK_INVENTORY`: instant inventory base table.
- `dbo.V_STK_INVLOTQUERY`: detail-like view over `T_STK_INVENTORY`.
- `dbo.V_STK_WARNSTOCK`: inventory summary/warning view.
- `dbo.V_SCM_StockWarnConSole`: inventory-related view over `T_STK_INVENTORY`.

Important quantity caveat:

- Do not assume `FQTY` is the business inventory quantity.
- Cross-check `FQTY`, `FBASEQTY`, `FSECQTY`, and `V_STK_WARNSTOCK` totals before choosing the quantity column.
- In the verified instant-inventory case, `FBASEQTY` matched the summary-view total while detail `FQTY` was zero.

Common inventory joins:

- Material code/name:
  - `T_BD_MATERIAL.FMATERIALID = inv.FMATERIALID`
  - `T_BD_MATERIAL_L.FMATERIALID = T_BD_MATERIAL.FMATERIALID`
  - `T_BD_MATERIAL_L.FLOCALEID = 2052`
- Warehouse name:
  - `T_BD_STOCK_L.FSTOCKID = inv.FSTOCKID`
  - `T_BD_STOCK_L.FLOCALEID = 2052`
- Stock unit:
  - `T_BD_UNIT_L.FUNITID = inv.FSTOCKUNITID`
  - `T_BD_UNIT_L.FLOCALEID = 2052`
- Stock status:
  - `T_BD_STOCKSTATUS_L.FSTOCKSTATUSID = inv.FSTOCKSTATUSID`
  - `T_BD_STOCKSTATUS_L.FLOCALEID = 2052`
- Stock organization:
  - `T_ORG_ORGANIZATIONS_L.FORGID = inv.FSTOCKORGID`
  - `T_ORG_ORGANIZATIONS_L.FLOCALEID = 2052`

## Auxiliary Attribute: Color

Verified path for inventory color-like auxiliary attribute:

```sql
inv.FAUXPROPID
  -> dbo.T_BD_FLEXSITEMDETAILV.FID
  -> dbo.T_BD_FLEXSITEMDETAILV.FF100001
  -> dbo.V_BAS_ASSISTANTDATAENTRY_L.fid
```

Use `V_BAS_ASSISTANTDATAENTRY_L.FLOCALEID = 2052` and `fname` for display values such as `黑色BK`, `宝蓝BU`, `透明TR`.

Some older sales-order SQL uses `T_BAS_ASSISTANTDATAENTRY_L.FENTRYID`; verify the exact key (`fid` vs `FENTRYID`) against the chosen source before writing a new view.

## Dependency Safety

- If a new `A_` view depends on an existing `A_` view, run `view-info` and a small `SELECT` against the upstream first.
- Binding errors usually mean the referenced object or column no longer exists.
- Prefer direct base/view sources for critical views unless the user explicitly wants chained views.

## Report Semantics

- Preserve negative quantities and report them. Do not hide them unless the user requests a positive-only operational report.
- Keep or drop zero-valued rows based on the requested report style. Screenshot-like inventory reports often exclude zero groups; complete master-data reports may retain them.
- If the requested total is known, compare the generated view total against it during validation.
