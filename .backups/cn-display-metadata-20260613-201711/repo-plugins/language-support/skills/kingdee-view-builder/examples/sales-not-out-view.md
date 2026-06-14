# Example: Sales Not-Out View

User request:

> 做个 A_ 开头的销售订单未出库视图，字段参考销售订单进度表，只筛选剩余未出数量大于 0 的订单。

Expected workflow:

- Locate sales-order sources and existing `A_`/sales views.
- Verify any upstream view dependency exists before using it.
- If an upstream dependency is missing, stop and offer to recreate or inline the source SQL.
- Keep output columns in Chinese business terms.
- Validate row count, sample rows, and quantity/amount sums after creation.
