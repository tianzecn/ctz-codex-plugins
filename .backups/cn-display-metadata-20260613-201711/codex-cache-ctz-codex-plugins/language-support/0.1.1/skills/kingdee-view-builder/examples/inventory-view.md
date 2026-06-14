# Example: Instant Inventory View

User request:

> 做一个以 A_ 开头的即时库存视图，列和截图一样：物料编码、物料名称、辅助属性、仓库名称、库存主单位、库存量(主单位)、库存状态、库存组织，并汇总库存总数。

Expected workflow:

- Search the data model for `即时库存`.
- Confirm live objects such as `T_STK_INVENTORY`, `V_STK_INVLOTQUERY`, and `V_STK_WARNSTOCK`.
- Cross-check `FQTY` vs `FBASEQTY` vs summary totals before selecting the stock quantity.
- Resolve auxiliary attribute display names through the flex/assistant-data path.
- Create a `dbo.A_*` view only after confirmation.
- Validate with `COUNT`, `TOP 20`, and automatic quantity `SUM`.
