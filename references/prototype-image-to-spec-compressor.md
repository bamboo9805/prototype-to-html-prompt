# 原型图 -> 结构化描述压缩器（PISC v2）

用于把“原型图截图 + 零散描述”压缩成可用于生成 HTML 报告 Prompt 的结构化输入。

## 输入

- 原型图（可多张）
- 用户补充（业务目标、接口、字段）

## 输出（固定 7 段）

```yaml
Goal:
  audience: ""
  topic: ""
  decision: ""

Layout:
  order: ["模块A", "模块B", "模块C"]
  modules:
    - name: ""
      type: "kpi|chart|table|filter|text"
      purpose: ""

DataContract:
  apis:
    - id: ""
      method: "GET|POST"
      url: ""
      params: { }
      responseKeys: [ ]
      auth: ""
  mapping:
    - ui: "模块.字段"
      api: "apiId.字段"

Interactions:
  controls: ["dateRange", "select", "search"]
  behaviors: ["filter", "sort", "paginate", "refresh"]
  states: ["loading", "empty", "error"]

VisualRules:
  style: "简洁商务"
  responsive: "mobile>=360, desktop>=1280"

Constraints:
  stack: "native-html|react-ts"
  output: "single-file|multi-file"
  allowLibs: []
  codeOnly: true

Acceptance:
  - "可直接运行"
  - "字段映射完整"
  - "状态处理完整"
```

## 压缩规则

1. 只提取页面里**看得见的事实**，不要猜接口字段。  
2. 每个模块只保留：`name/type/purpose` 三项。  
3. 接口字段只保留“实现必需字段”，不要抄整段 schema。  
4. 非关键视觉描述压缩为 1 行（如“简洁商务风”）。  
5. 信息不足统一进入 `Missing Info`，不要硬补。

## 缺失项提问模板（最多 6 个）

- Q1 哪些模块需要真实接口，哪些可用静态示例？
- Q2 每个模块对应哪个 API？
- Q3 表格/图表主字段分别是什么？
- Q4 筛选条件与默认时间范围是什么？
- Q5 技术栈是原生 HTML 还是 React+TS？
- Q6 输出只要代码，还是先方案后代码？
