# 业务专属 Prompt 生成器 v2（中文注释版）

## 目标

用结构化 JSON 自动拼出“短、准、可执行”的 Prompt，降低人工描述成本和 token 浪费。

## 使用方式

1. 先用 `references/business-api-profile.template.json` 填你的业务信息（或复制 `references/business-api-profile.example.json` 作为起点）。
2. 保存为业务文件（例如 `my-report.json`）。
3. 运行：

```bash
python scripts/build_prompt_v2.py --input my-report.json --output final-prompt.txt
```

4. 将 `final-prompt.txt` 直接粘贴到 Cursor/Codex/Claude Code。

## 设计要点

- 输入是结构化 JSON，避免自由文本歧义。
- 输出 Prompt 固定段落：目标/模块/接口/映射/交互/约束/验收/输出协议。
- 自动标记缺失字段（`# Missing`），避免“看起来可用，实际缺关键信息”。

## 建议协作流程

- 产品/设计：维护 `prototype.modules` + `goal`
- 后端：维护 `apis`
- 前端：维护 `mapping` + `acceptance`
- AI 协作者：只消费 `final-prompt.txt`
