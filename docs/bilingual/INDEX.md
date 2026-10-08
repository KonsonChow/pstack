# pstack 中英对照学习版

本版依据上游 commit `157aae39a733135e93d8b5b19ff62c6a84b0ad56`，覆盖原仓库全部 127 份 Markdown 文档，共 2,511 个对照单元。一般按空行分段；列表、表格、frontmatter 和代码块保持为完整单元。

正文按英文在前、中文在后的顺序上下对照，用语言和段落位置区分原文与译文，不加逐段标签或引用边框。英文标题保留标题层级，中文标题作为加粗副标题紧随其后。同文的命令、代码及结构标记只展示一次；同一张图片只展示一次，替代文字保留双语说明。命令、路径、API、配置键、模型 slug 和必要术语保留原文；自然语言示例提示词及说明注释按工程语境翻译。英文源文件保持不变。图片和代码文件链接指回原仓库对应文件，文档间的链接优先进入对照版。

建议先读[项目总览](./README.md)、[术语表](./GLOSSARY.md)和[使用指南](./docs/guide/README.md)，再读 [`poteto-mode`](./skills/poteto-mode/SKILL.md)、工程原则与具体执行规程。[原文假设与技术注记](./SOURCE_NOTES.md)单独说明原文中的冲突、技术局限及环境前提。

这里的译文用于学习与对照。插件安装仍读取原来的 `skills/` 和 `agents/`，翻译文件中的指令是在介绍原文，不会因生成学习版而自动执行。

## 维护翻译

段落译文与源文快照保存在仓库根目录的 `translations/zh-CN/<原路径>.json`。编辑对应的 `zh` 字段，再在仓库根目录运行：

```bash
python3 scripts/bilingual.py build
python3 scripts/bilingual.py check
```

`build` 生成对照 Markdown。`check` 校验 127 份文档的覆盖、中文字段、原文拼接、源文件 SHA256、标题和链接目标，并确认已生成文件与译文数据一致。上游原文变化会使检查失败，需要重新分段并审校译文；脚本不会自动把旧译文认定为适配新版本。代码与占位符可以保留英文，自动检查不能代替工程语义审校。

术语可以在翻译中追加或修正。修改[术语表](./GLOSSARY.md)后，应同时复核使用该术语的译文。

## 总览与同步（2 份）

- [MIRROR.md](./MIRROR.md)
- [README.md](./README.md)

## 使用指南（11 份）

- [docs/guide/01-setup.md](./docs/guide/01-setup.md)
- [docs/guide/02-poteto-mode.md](./docs/guide/02-poteto-mode.md)
- [docs/guide/03-understand.md](./docs/guide/03-understand.md)
- [docs/guide/04-design.md](./docs/guide/04-design.md)
- [docs/guide/05-build-and-clean.md](./docs/guide/05-build-and-clean.md)
- [docs/guide/06-verify-and-ship.md](./docs/guide/06-verify-and-ship.md)
- [docs/guide/07-overnight.md](./docs/guide/07-overnight.md)
- [docs/guide/08-principles.md](./docs/guide/08-principles.md)
- [docs/guide/09-make-it-yours.md](./docs/guide/09-make-it-yours.md)
- [docs/guide/10-recipes-and-pitfalls.md](./docs/guide/10-recipes-and-pitfalls.md)
- [docs/guide/README.md](./docs/guide/README.md)

## 工程原则（23 份）

- [skills/principle-attack-the-premise/SKILL.md](./skills/principle-attack-the-premise/SKILL.md)
- [skills/principle-boundary-discipline/SKILL.md](./skills/principle-boundary-discipline/SKILL.md)
- [skills/principle-build-the-lever/SKILL.md](./skills/principle-build-the-lever/SKILL.md)
- [skills/principle-encode-lessons-in-structure/SKILL.md](./skills/principle-encode-lessons-in-structure/SKILL.md)
- [skills/principle-exhaust-the-design-space/SKILL.md](./skills/principle-exhaust-the-design-space/SKILL.md)
- [skills/principle-experience-first/SKILL.md](./skills/principle-experience-first/SKILL.md)
- [skills/principle-fix-root-causes/SKILL.md](./skills/principle-fix-root-causes/SKILL.md)
- [skills/principle-foundational-thinking/SKILL.md](./skills/principle-foundational-thinking/SKILL.md)
- [skills/principle-guard-the-context-window/SKILL.md](./skills/principle-guard-the-context-window/SKILL.md)
- [skills/principle-laziness-protocol/SKILL.md](./skills/principle-laziness-protocol/SKILL.md)
- [skills/principle-make-operations-idempotent/SKILL.md](./skills/principle-make-operations-idempotent/SKILL.md)
- [skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md](./skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md)
- [skills/principle-minimize-reader-load/SKILL.md](./skills/principle-minimize-reader-load/SKILL.md)
- [skills/principle-model-the-domain/SKILL.md](./skills/principle-model-the-domain/SKILL.md)
- [skills/principle-never-block-on-the-human/SKILL.md](./skills/principle-never-block-on-the-human/SKILL.md)
- [skills/principle-outcome-oriented-execution/SKILL.md](./skills/principle-outcome-oriented-execution/SKILL.md)
- [skills/principle-prove-it-works/SKILL.md](./skills/principle-prove-it-works/SKILL.md)
- [skills/principle-redesign-from-first-principles/SKILL.md](./skills/principle-redesign-from-first-principles/SKILL.md)
- [skills/principle-separate-before-serializing-shared-state/SKILL.md](./skills/principle-separate-before-serializing-shared-state/SKILL.md)
- [skills/principle-sequence-verifiable-units/SKILL.md](./skills/principle-sequence-verifiable-units/SKILL.md)
- [skills/principle-subtract-before-you-add/SKILL.md](./skills/principle-subtract-before-you-add/SKILL.md)
- [skills/principle-test-behavior-not-implementation/SKILL.md](./skills/principle-test-behavior-not-implementation/SKILL.md)
- [skills/principle-type-system-discipline/SKILL.md](./skills/principle-type-system-discipline/SKILL.md)

## 执行规程（23 份）

- [skills/poteto-mode/playbooks/authoring-a-skill.md](./skills/poteto-mode/playbooks/authoring-a-skill.md)
- [skills/poteto-mode/playbooks/autonomous-run.md](./skills/poteto-mode/playbooks/autonomous-run.md)
- [skills/poteto-mode/playbooks/autopilot-full.md](./skills/poteto-mode/playbooks/autopilot-full.md)
- [skills/poteto-mode/playbooks/autopilot-stack.md](./skills/poteto-mode/playbooks/autopilot-stack.md)
- [skills/poteto-mode/playbooks/babysit.md](./skills/poteto-mode/playbooks/babysit.md)
- [skills/poteto-mode/playbooks/bug-fix.md](./skills/poteto-mode/playbooks/bug-fix.md)
- [skills/poteto-mode/playbooks/eval.md](./skills/poteto-mode/playbooks/eval.md)
- [skills/poteto-mode/playbooks/feature.md](./skills/poteto-mode/playbooks/feature.md)
- [skills/poteto-mode/playbooks/hillclimb.md](./skills/poteto-mode/playbooks/hillclimb.md)
- [skills/poteto-mode/playbooks/investigation.md](./skills/poteto-mode/playbooks/investigation.md)
- [skills/poteto-mode/playbooks/multi-phase-plan.md](./skills/poteto-mode/playbooks/multi-phase-plan.md)
- [skills/poteto-mode/playbooks/opening-a-pr.md](./skills/poteto-mode/playbooks/opening-a-pr.md)
- [skills/poteto-mode/playbooks/orchestrate.md](./skills/poteto-mode/playbooks/orchestrate.md)
- [skills/poteto-mode/playbooks/pause-safely.md](./skills/poteto-mode/playbooks/pause-safely.md)
- [skills/poteto-mode/playbooks/perf-issue.md](./skills/poteto-mode/playbooks/perf-issue.md)
- [skills/poteto-mode/playbooks/prototype.md](./skills/poteto-mode/playbooks/prototype.md)
- [skills/poteto-mode/playbooks/refactoring.md](./skills/poteto-mode/playbooks/refactoring.md)
- [skills/poteto-mode/playbooks/runtime-forensics.md](./skills/poteto-mode/playbooks/runtime-forensics.md)
- [skills/poteto-mode/playbooks/session-pickup.md](./skills/poteto-mode/playbooks/session-pickup.md)
- [skills/poteto-mode/playbooks/shipping.md](./skills/poteto-mode/playbooks/shipping.md)
- [skills/poteto-mode/playbooks/trace-forensics.md](./skills/poteto-mode/playbooks/trace-forensics.md)
- [skills/poteto-mode/playbooks/visual-parity.md](./skills/poteto-mode/playbooks/visual-parity.md)
- [skills/poteto-mode/playbooks/worktree-cleanup.md](./skills/poteto-mode/playbooks/worktree-cleanup.md)

## Skills 与参考材料（55 份）

- [skills/architect/SKILL.md](./skills/architect/SKILL.md)
- [skills/architect/references/design-red-flags.md](./skills/architect/references/design-red-flags.md)
- [skills/architect/references/rationale-template.md](./skills/architect/references/rationale-template.md)
- [skills/architect/references/runner-prompt.md](./skills/architect/references/runner-prompt.md)
- [skills/arena/SKILL.md](./skills/arena/SKILL.md)
- [skills/automate-me/SKILL.md](./skills/automate-me/SKILL.md)
- [skills/blast-radius/SKILL.md](./skills/blast-radius/SKILL.md)
- [skills/bro/SKILL.md](./skills/bro/SKILL.md)
- [skills/create-verification-skill/SKILL.md](./skills/create-verification-skill/SKILL.md)
- [skills/create-verification-skill/references/feature-map-example/README.md](./skills/create-verification-skill/references/feature-map-example/README.md)
- [skills/create-verification-skill/references/feature-map-example/create-note.md](./skills/create-verification-skill/references/feature-map-example/create-note.md)
- [skills/create-verification-skill/references/feature-map-example/search.md](./skills/create-verification-skill/references/feature-map-example/search.md)
- [skills/figure-it-out/SKILL.md](./skills/figure-it-out/SKILL.md)
- [skills/how/SKILL.md](./skills/how/SKILL.md)
- [skills/how/references/explainer-prompt.md](./skills/how/references/explainer-prompt.md)
- [skills/how/references/explorer-prompt.md](./skills/how/references/explorer-prompt.md)
- [skills/interrogate/SKILL.md](./skills/interrogate/SKILL.md)
- [skills/interrogate/references/code-quality-review.md](./skills/interrogate/references/code-quality-review.md)
- [skills/interrogate/references/lead-judgment.md](./skills/interrogate/references/lead-judgment.md)
- [skills/interrogate/references/reviewer-prompt.md](./skills/interrogate/references/reviewer-prompt.md)
- [skills/interrogate/references/rubric.md](./skills/interrogate/references/rubric.md)
- [skills/maintain-verification-skill/SKILL.md](./skills/maintain-verification-skill/SKILL.md)
- [skills/make-bot-ui/SKILL.md](./skills/make-bot-ui/SKILL.md)
- [skills/no-comments/SKILL.md](./skills/no-comments/SKILL.md)
- [skills/no-comments/references/comment-sicko.md](./skills/no-comments/references/comment-sicko.md)
- [skills/poteto-mode/SKILL.md](./skills/poteto-mode/SKILL.md)
- [skills/poteto-mode/references/bugbot-triage.md](./skills/poteto-mode/references/bugbot-triage.md)
- [skills/recall/SKILL.md](./skills/recall/SKILL.md)
- [skills/reflect/SKILL.md](./skills/reflect/SKILL.md)
- [skills/reflect/references/divergent-reviewer.md](./skills/reflect/references/divergent-reviewer.md)
- [skills/reflect/references/judgment-reviewer.md](./skills/reflect/references/judgment-reviewer.md)
- [skills/reflect/references/synthesizer.md](./skills/reflect/references/synthesizer.md)
- [skills/reflect/references/tooling-reviewer.md](./skills/reflect/references/tooling-reviewer.md)
- [skills/setup-pstack/SKILL.md](./skills/setup-pstack/SKILL.md)
- [skills/show-me-your-work/SKILL.md](./skills/show-me-your-work/SKILL.md)
- [skills/swarm/SKILL.md](./skills/swarm/SKILL.md)
- [skills/tdd/SKILL.md](./skills/tdd/SKILL.md)
- [skills/teach/SKILL.md](./skills/teach/SKILL.md)
- [skills/technical-writing/SKILL.md](./skills/technical-writing/SKILL.md)
- [skills/typescript-best-practices/SKILL.md](./skills/typescript-best-practices/SKILL.md)
- [skills/typescript-best-practices/references/patterns.md](./skills/typescript-best-practices/references/patterns.md)
- [skills/unslop/SKILL.md](./skills/unslop/SKILL.md)
- [skills/why/SKILL.md](./skills/why/SKILL.md)
- [skills/why/references/epistemics.md](./skills/why/references/epistemics.md)
- [skills/why/references/investigator-prompt.md](./skills/why/references/investigator-prompt.md)
- [skills/why/references/source-playbook.md](./skills/why/references/source-playbook.md)
- [skills/why/references/sources/code-archaeology.md](./skills/why/references/sources/code-archaeology.md)
- [skills/why/references/sources/databricks.md](./skills/why/references/sources/databricks.md)
- [skills/why/references/sources/datadog.md](./skills/why/references/sources/datadog.md)
- [skills/why/references/sources/incident-postmortem.md](./skills/why/references/sources/incident-postmortem.md)
- [skills/why/references/sources/linear.md](./skills/why/references/sources/linear.md)
- [skills/why/references/sources/notion.md](./skills/why/references/sources/notion.md)
- [skills/why/references/sources/sentry.md](./skills/why/references/sources/sentry.md)
- [skills/why/references/sources/slack.md](./skills/why/references/sources/slack.md)
- [skills/why/references/synthesizer-prompt.md](./skills/why/references/synthesizer-prompt.md)

## Agent 角色（2 份）

- [agents/comment-sicko.md](./agents/comment-sicko.md)
- [agents/poteto-agent.md](./agents/poteto-agent.md)

## Benny 自动化（11 份）

- [automations/benny/FOR_AGENTS.md](./automations/benny/FOR_AGENTS.md)
- [automations/benny/README.md](./automations/benny/README.md)
- [automations/benny/skills/reproduce-and-fix-issues/SKILL.md](./automations/benny/skills/reproduce-and-fix-issues/SKILL.md)
- [automations/benny/skills/reproduce-and-fix-issues/references/control-adapter.md](./automations/benny/skills/reproduce-and-fix-issues/references/control-adapter.md)
- [automations/benny/skills/reproduce-and-fix-issues/references/feature-map.example.md](./automations/benny/skills/reproduce-and-fix-issues/references/feature-map.example.md)
- [automations/benny/skills/reproduce-and-fix-issues/references/verify-existing-fix.md](./automations/benny/skills/reproduce-and-fix-issues/references/verify-existing-fix.md)
- [automations/benny/skills/setup-benny/SKILL.md](./automations/benny/skills/setup-benny/SKILL.md)
- [automations/benny/skills/triage-issue-reports/SKILL.md](./automations/benny/skills/triage-issue-reports/SKILL.md)
- [automations/benny/skills/triage-issue-reports/references/routing.example.md](./automations/benny/skills/triage-issue-reports/references/routing.example.md)
- [automations/benny/templates/reproduce-automation-prompt.md](./automations/benny/templates/reproduce-automation-prompt.md)
- [automations/benny/templates/triage-automation-prompt.md](./automations/benny/templates/triage-automation-prompt.md)
