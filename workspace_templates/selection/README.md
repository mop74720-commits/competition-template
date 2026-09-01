# Selection Workspace

临时探索区，用于多题/多路线选择。它不是正式 Competition Repo，也不是本场比赛事实源。

允许：临时假设、失败 probe、候选路线、未验证参数、快速代码和比较记录。
禁止：把这里的猜测直接当正式 FACT。

核心文件：`SELECTION_STATUS.md / PROBLEM_CARDS.md / ROUTE_CARDS.md / PROBE_LEDGER.csv / DECISION.md`。

选定题后冻结/归档；`promote_selection.py` 只把决策证据写入正式 Repo 的 `audit/selection/`，不会自动晋升事实。
