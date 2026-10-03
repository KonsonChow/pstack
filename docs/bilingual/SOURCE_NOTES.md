# 阅读时需要区分的原文假设

这些说明是学习版的编者注，不属于上游原文。对照译文保留了原文主张，没有用编者判断替换它。

## 决策日志的两条要求存在张力

[`show-me-your-work`](./skills/show-me-your-work/SKILL.md) 要求日志只追加，错误决定用新行覆盖说明，不能修改或删除历史；但末尾审计步骤又要求删去编造、愿望式或凑数条目。这两项要求如何同时落实，原文没有明确交代。学习时应区分纠正历史事实与整理交付材料，而不要把译文中的两条指令误认成已经解决的统一规则。

## Hillclimb 的日志格式与共享 skill 不一致

[`hillclimb`](./skills/poteto-mode/playbooks/hillclimb.md) 要求通过 `show-me-your-work` 建立决策日志，却又列出独立的 `decision.tsv` 列格式。[`show-me-your-work`](./skills/show-me-your-work/SKILL.md) 则要求由它统一管理格式，不要重新声明列。对照版保留了两处内容，实际采用时需要决定是维护独立实验记录，还是扩展统一日志。

## 起点加持续时间并不自动排除负数

[TypeScript 示例](./skills/typescript-best-practices/references/patterns.md) 用 `TimeRange = { start: Date; durationMs: number }` 替代起止时间，并声称负时间区间无法构造。但普通 `number` 仍允许负值，例如 `durationMs: -1`。表示方式消除了两个时间戳的顺序维护问题，却没有单靠这个类型保证持续时间非负。若需要这个保证，还须在创建边界校验，或使用承载该约束的类型。中文对照保留原注释，避免悄悄改变原文。

## 工具与模型描述依赖原作者的环境

[`why`](./skills/why/SKILL.md) 等文档包含对 git、gh、MCP、Ask 模式及云端 agent 的环境假设。模型名称、slug、Cursor 路径和命令也按原文保留。它们描述的是该版本体系的运行约定，不能仅凭译文就推定所有 agent 宿主都具备相同能力。

## MIRROR 中的 upstream 是分支名

[`MIRROR.md`](./MIRROR.md) 描述 `backnotprop/pstack` 自身如何同步 `cursor/plugins/pstack`，其中的 `upstream` 是用于保存 Cursor 原文件的分支。当前 fork 的 Git remote `upstream` 指向 `backnotprop/pstack`，两者不是同一个概念。阅读同步命令时要辨明它描述的仓库层级。

## 一个链接是模板占位符

[`why` 综合提示词](./skills/why/references/synthesizer-prompt.md) 含有 Markdown 链接目标 `url`。这是引用格式示例，不是真实仓库路径。链接检查将它记录为源文档占位符，不把它当作翻译引入的失效链接。
