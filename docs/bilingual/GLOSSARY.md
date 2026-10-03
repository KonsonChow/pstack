# 翻译术语与表达约定

按软件工程语境理解后翻译。保留原文的约束强度、前置条件、例外、证据要求及角色分工。不得把 must 改成建议，不得为原文添加保证。中文采用简体。

| English | 中文约定 | 使用说明 |
|---|---|---|
| agent | agent / 智能体 | 常用 agent；首次解释为执行任务的 AI 智能体 |
| subagent | subagent / 子智能体 | 保留角色名及 API 名 |
| skill | skill / 技能 | 作为可调用能力时保留 skill；具体名称原样保留 |
| mode | 工作模式 | poteto-mode 等名称不翻译 |
| playbook | 执行规程 | 指按任务类型组织的操作步骤，不译为剧本 |
| harness | agent 运行环境 | 指宿主工具及其工具调用、权限、上下文机制 |
| wrapper | 封装层 | 若是具体文件或类型，保留标识符 |
| delegate | 委派 / 委派执行者 | 按动词或角色区分 |
| orchestrate / orchestration | 协调执行 / 任务协调 | 涉及多 agent 的分工、依赖和状态管理 |
| fan out | 分派并行任务 | 不译为扇出，除非描述网络拓扑 |
| drain | 等待所有并行任务结束并收齐结果 | 根据上下文简写为收齐结果 |
| panel | 评审组 | 多模型独立审查的组合 |
| judgment | 判断 / 评审判断 | 不能一律译为审判 |
| head | 分支当前提交 / HEAD | exact head 是指定的完整 commit SHA |
| stack | PR 栈 / 提交栈 | 根据上下文区分；pstack 是项目名 |
| stacked PRs | 有依赖关系的 PR 栈 | 上一 PR 的分支是下一 PR 的基线 |
| base / base branch | 基线 / 基线分支 | 与 head 区分 |
| land | 合入 / 合入目标分支 | 一般表示实际合并，不等于提交或推送 |
| ship | 交付 / 发布 / 合入 | 按实际动作判断，不能默认等于部署 |
| merge-ready | 满足合并条件 | 不意味着已经合并 |
| gate | 检查关卡 / 必须通过的检查 | 保留阻止后续动作的含义 |
| green | 检查通过 | green CI 不等于行为已验证 |
| flaky / flake | 不稳定 / 偶发失败 | 描述测试或 CI 的非确定性失败 |
| repro / reproduce | 复现 | 先复现、再修复的顺序须保留 |
| regression | 回归问题 | regression test 为回归测试 |
| root cause | 根因 | 不能把掩盖症状译成修复根因 |
| runtime evidence | 运行时证据 | 真实运行的输出、日志、截图或观测 |
| verification | 验证 | 证明实际行为符合要求 |
| validation | 校验 / 验证 | 数据边界检查用校验，验收用验证 |
| artifact | 产物 / 证据文件 | 指构建产物、文档、trace 等，按上下文选择 |
| trace | trace / 执行追踪 | 保留 cpuprofile、spindump 等格式名 |
| hillclimb | hillclimb / 迭代优化 | 通过假设、测量和保留有效改动持续改善指标 |
| baseline | 基准 / 基线 | 性能测量为基准，分支与版本为基线 |
| invariant | 不变量 | 系统始终成立的约束 |
| seam | 边界 / 可替换边界 | 接口或模块职责边界，不机械译为接缝 |
| deep module | 深模块 | 用小而稳定的接口封装较复杂的实现 |
| blast radius | 影响范围 | 改动可能影响的调用方、行为和系统部分 |
| scope | 范围 / 作用域 | 任务范围与变量作用域需区分 |
| source of truth | 权威来源 | 也可依上下文写唯一权威数据来源 |
| provenance | 来源记录 / 来源依据 | 证据来源与生成过程 |
| epistemics | 证据与认知边界 | 关注已知事实、推断及不确定性 |
| contract | 约定 / 契约 | 操作约定与 API 契约按上下文区分 |
| idempotent | 幂等 | 重复执行收敛到同一状态 |
| scaffold | 基础结构 / 初始骨架 | 根据是否指生成项目框架判断 |
| slop | 粗糙冗余的 AI 产物 | 代码语境可用低质代码，写作语境可用 AI 套话 |
| unslop / deslop | 清理 AI 套话 / 清理低质代码 | skill 名和命令原样保留 |
| consumer / maintainer | 使用者 / 维护者 | 模块调用方可译为调用方 |
| control skill | 操作与验证 skill | 驱动真实 UI 或 CLI，不是权限控制 |
| feature map | 功能验证清单 | 功能到验证操作和证据的映射 |
| worktree | worktree / 工作树 | Git 命令与路径原样保留 |

英文段落逐段保留，每段后跟中文。标题、列表、表格、注释中承载的说明文字也翻译。代码、命令、路径、API、模型名及配置键原样保留；面向 agent 的自然语言示例提示词和 YAML description 在中文段落中翻译。代码块中的说明注释可以译成中文，但不能改动可执行语义。纯结构 HTML 标签、分隔线、无自然语言的命令块可原样对应。原文如果有过时声明或失效链接，忠实翻译并交给主 agent 记录，不擅自修正原意。

本次翻译追加的术语：

| English | 中文约定 | 使用说明 |
|---|---|---|
| merge frontier | 合并前沿 | PR 栈中最靠栈底、尚未合入的 PR；不是最新创建的 PR |
| forge | 代码托管平台 | 例如 GitHub、Origin，保留具体平台名 |
| effort | 推理强度 / 工作投入 | 模型配置用推理强度，任务预算按语境用工作投入 |
| slug | slug / 标识 | 模型 slug、路径 slug 保留具体值，不翻译成自然语言 |
| fail closed | 条件不足时拒绝继续 | 缺少能力、配置或证据时，不继续执行有副作用的动作 |
| discriminating state | 能区分正常与异常行为的关键状态 | 防止把中间加载状态、预期对话框误认为 bug |
| rejection window | 异议窗口 | 等待他人指出复现条件或判断有误的时间段 |
| smoke / smoke test | 冒烟检查 / 冒烟测试 | 快速检查相关关键路径是否仍可用 |

| English | 中文约定 | 使用说明 |
|---|---|---|
| total function | 全函数 | 对其允许的每个输入都有定义，不会因为未建模的输入情况而失效 |
| total type | 满足操作全定义要求的类型 | 原文强调目标操作对每个合法输入都有定义，不是类型系统的“完备性” |
| partiality | 偏函数行为 / 某些合法输入下操作无定义 | 按上下文解释，不译为“部分性” |
| constructive modeling | 构造式建模 | 通过表示方式构造合法状态，而不靠事后剔除非法组合 |
| temporal decomposition | 按执行时序拆分 | 以“先做、再做、最后做”组织模块，可能拆散同一领域知识 |
| characterization test | 刻画现有行为的测试 | 在重构前记录实际行为，作为保持行为的基准 |
| pin behavior | 固定行为基准 / 锁定现有行为 | 通过可执行检查约束重构，不能理解为固定实现 |
| receipts | 执行证据 / 证据记录 | 指命令输出、测试记录、截图等，不是身份认证凭据 |
| credentials | 身份认证凭据 | token、密钥或其他访问身份信息，须与 receipts 区分 |
