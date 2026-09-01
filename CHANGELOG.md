# Changelog

## 0.1.1

2020C 全系统演练修复：

- 新增 `contest_import.py`，复制/哈希原始题面和附件并生成 advisory preflight；
- DOCX 同时读取 python-docx 可见结构与 OOXML 全文本，降低文本框/对象漏读风险；
- PDF 支持文本量检查与可选页面渲染，不默认 OCR；
- 自动提取数字、范围、上下限和单位候选，但不自动升级为 FACT；
- 新增 `SOURCE_MANIFEST.csv` / `PREFLIGHT_REPORT.md`；
- 新增可选 `results/final/submission/` staging 位置；
- AI usage log 改为只记录重大 AI 介入，避免形成流程负担。
