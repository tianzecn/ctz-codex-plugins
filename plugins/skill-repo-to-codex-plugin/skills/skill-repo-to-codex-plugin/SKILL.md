---
name: skill-repo-to-codex-plugin
description: |
  当用户想把上游 GitHub skill 仓库或新 skill 需求做成目标 Codex 插件市场仓库中的插件/技能时使用。若用户没有指定目标插件，先参考 references/plugin-category-table.md 自动判断所属分类与能力型插件，再导入或创建 skill，更新 marketplace，校验后 commit、push，并执行 codex plugin marketplace upgrade。
---

# Skill Repo to Codex Plugin

你负责把一个上游 GitHub skill 仓库或新 skill 需求打包到目标 Codex 插件市场仓库里的正确能力型插件中。默认用中文汇报。

执行本技能时，必须先使用 `$plugin-creator`，并遵循它对 `.codex-plugin/plugin.json`、`skills/`、`.agents/plugins/marketplace.json`、marketplace 条目字段和校验方式的要求。

## 输入变量

- `upstream_repo`: 可选。用户提供上游 GitHub skill 仓库 URL 或 `owner/repo` 时使用。
- `skill_request`: 可选。用户要求创建一个新 skill、但没有给上游仓库时，用用户需求作为 skill 设计输入。
- `target_repo`: 默认 `tianzecn/ctz-codex-plugins`。
- `plugin_name`: 可选。用户明确指定目标插件时使用；未指定时必须先参考 `references/plugin-category-table.md` 自动判断所属 `Category` 与能力型 `Plugins`，再把选中的插件名规范化为 kebab-case。
- `marketplace_name`: 默认读取目标仓库 `.agents/plugins/marketplace.json` 的 `name`，通常是 `ctz-codex-plugins`。

如果同时缺少 `upstream_repo` 和 `skill_request`，先问用户要 GitHub 链接或新 skill 需求；不要把占位变量当成真实输入。

## 成功标准

完成后必须满足：

1. 交付在 GitHub 目标仓库里，不只是本地插件。
2. 目标仓库新增或更新 `plugins/<plugin-name>/`，包含 `.codex-plugin/plugin.json` 和 `skills/`。
3. 更新 `.agents/plugins/marketplace.json`，把新插件加入 `plugins[]`。
4. 如果用户没有指定 `plugin_name`，最终回复必须说明自动判断出的 `Category`、能力型插件名、判断依据，以及是否创建了新插件还是追加到已有插件。
5. 优先读取上游已有 `.claude-plugin/marketplace.json`、`.codex-plugin/plugin.json`、`.claude-plugin/plugin.json`、`skills/*/SKILL.md`，按上游声明导入 skills。
6. 新 skill 需求没有上游仓库时，按用户需求创建最小 `SKILL.md`，并把资源只放在对应 skill 目录下。
7. 跳过明确标注 Deprecated 的技能，除非用户要求保留。
8. 插件 manifest 和 marketplace 条目必须是真实信息，不留下占位字段。
9. 插件必须有市场图标：`interface.logo` 和 `interface.composerIcon` 都指向存在的相对路径，默认使用 `./assets/icon.svg`。
10. 校验 JSON、skill frontmatter、图标路径和 `git diff --check`。
11. commit 并 push 到目标 GitHub 仓库。
12. 执行 `codex plugin marketplace upgrade <marketplace_name>`，确认远程缓存能看到新插件。
13. 最终告诉用户 commit hash、导入了几个 skills、Codex App 里应该选哪个远程 marketplace 入口。

## 工作流

### 1. 准备目标仓库

- 找到或克隆 `target_repo`，优先复用本机已有干净副本。
- 运行 `git status --short --branch`。如果已有无关改动，先说明并避免覆盖；如果会阻塞本次写入，询问用户。
- 读取 `.agents/plugins/marketplace.json`，确认 marketplace 名称和现有插件结构。
- 先使用 `$plugin-creator` 读取规则，但在确定 `plugin_name` 之前不要创建脚手架。
- 读取 `references/plugin-category-table.md`。该表的 `Category` 是 marketplace/interface 的用户可见大类，`Plugins` 是能力型插件包候选。

### 2. 读取上游声明或新 skill 需求

如果有 `upstream_repo`，克隆或拉取到临时目录。按以下优先级收集信息：

1. `.codex-plugin/plugin.json`
2. `.claude-plugin/plugin.json`
3. `.claude-plugin/marketplace.json`
4. `skills/*/SKILL.md`

从上游元数据推导：

- 插件名、显示名、描述、作者、主页、license、keywords。
- skills 路径。如果 manifest 声明了 `skills`，以声明路径为准；否则扫描 `skills/*/SKILL.md`。
- 上游 marketplace 如果声明了本地 plugin 路径，进入对应路径继续查找该 plugin 的 manifest 和 skills。

如果没有 `upstream_repo`，根据 `skill_request` 提炼：

- skill 名称、触发场景、适用边界、执行流程、验证方式。
- 需要创建的 `SKILL.md` 与可选 `references/`、`scripts/`。
- 不要臆造外部仓库、license 或作者；无法确认的字段用当前目标插件的默认元数据或 `NOASSERTION`。

### 3. 自动判断所属分类与能力型插件

如果用户没有明确指定 `plugin_name`，必须先参考 `references/plugin-category-table.md`：

1. 读取上游 `README.md`、`SKILL.md` frontmatter、技能正文、目录名、关键词；新 skill 则读取 `skill_request`。
2. 在分类表中选择最贴近的 `Category` 与 `Plugins` 项。`Plugins` 项是能力型插件包名称，不是具体产品名。
3. 将选中的 `Plugins` 名称规范化为 kebab-case，作为目标 `plugin_name`。例如 `Architecture Design` -> `architecture-design`，`Text Processing` -> `text-processing`。
4. 如果目标仓库已存在 `plugins/<plugin-name>/`，把 skill 追加到该插件。
5. 如果目标仓库不存在该插件，使用 `$plugin-creator` 创建新的能力型插件，并用分类表中的插件名作为 `interface.displayName`，用分类表中的 `Category` 作为 `interface.category`。marketplace 条目的 `category` 仍按仓库默认使用 `Productivity`，除非用户明确要求改市场分类。
6. 如果一个 skill 同时命中多个插件，优先选择“用户会去哪里找它”的主工作流，而不是实现细节。例如 WebView 桌面架构应归 `Software Engineering / Architecture Design`，不是 `Design & Creative / UI Design`。
7. 只有在两个候选都同样合理且会导致不同目标插件时，才向用户确认；否则自动选择，并在最终回复说明判断依据。

如果用户明确指定了 `plugin_name`，跳过自动选择，但仍可用分类表补充 `interface.category` 和最终说明。

### 4. 选择要导入或创建的 skills

导入或创建规则：

- 只导入包含 `SKILL.md` 的 skill 目录，并连同该目录下的 `references/`、`scripts/`、`agents/`、`prompts/` 等相对资源一起复制。
- 如果上游仓库根目录本身就是一个 skill，且根目录存在 `SKILL.md`，导入为 `skills/<frontmatter-name-or-normalized-repo-name>/`，并复制根目录下的相对资源。
- 新 skill 需求应创建一个独立 `skills/<skill-name>/SKILL.md`，必要时加最少量 `references/`；不要创建未被用户要求的脚本或复杂目录。
- 如果 `SKILL.md` frontmatter 或开头说明明确包含 `deprecated: true`、`status: deprecated`、`Deprecated`、`DEPRECATED`、`已废弃`，跳过。
- 如果用户明确要求保留 deprecated skill，才导入，并在最终说明中单独列出。
- 不导入 `.git`、缓存目录、构建产物、大型依赖目录，例如 `node_modules/`、`.venv/`、`dist/`、`build/`、`__pycache__/`。
- 若同名 skill 已存在于目标插件目录，先比较内容；没有用户确认不要覆盖非本次生成的内容。

### 5. 生成或更新目标插件

在目标仓库创建：

```text
plugins/<plugin-name>/
  .codex-plugin/plugin.json
  assets/icon.svg
  skills/<skill-name>/SKILL.md
```

`plugin.json` 要求：

- `name` 与外层插件目录名一致。
- `version` 优先用上游 manifest 版本；没有则用 `0.1.0`。
- `description`、`author`、`homepage`、`repository`、`license`、`keywords` 都使用可核对的信息。
- `repository` 填目标仓库 URL；`homepage` 或 `websiteURL` 优先填上游仓库 URL。
- `skills` 固定为 `./skills/`。
- `interface.defaultPrompt` 最多 3 条，每条不超过 128 字符。
- `interface.logo` 和 `interface.composerIcon` 都必须存在。默认设为 `./assets/icon.svg`。
- 不保留占位字段、空描述或明显虚构字段。无法确认的 license 用 `NOASSERTION`，不要伪造。
- 如果是更新已有插件，且新增 skill、图标或用户可见 metadata 发生变化，应将插件版本号做 patch bump，除非上游 manifest 已提供更高版本。
- 如果自动归类创建的是能力型插件，插件 manifest 应表达该能力包本身，而不是只复述某个单一上游仓库；上游仓库信息放进被导入 skill 的来源说明里。

图标生成要求：

- 如果上游 manifest 已声明 `logo` / `composerIcon` 且对应资产可复制，优先保留上游资产，并保证路径相对插件根目录、以 `./` 开头。
- 如果上游没有可用图标，创建 `plugins/<plugin-name>/assets/icon.svg`。图标应是轻量 SVG，使用插件 `brandColor` 或从主题推导的单一主色，包含简短字母或抽象符号即可。
- 不要下载或伪造官方商标。没有明确授权或上游资产时，用抽象图形。
- `logo` 和 `composerIcon` 可以指向同一个 `./assets/icon.svg`，除非上游提供了不同尺寸资产。

marketplace 条目要求：

```json
{
  "name": "<plugin-name>",
  "source": {
    "source": "local",
    "path": "./plugins/<plugin-name>"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Productivity"
}
```

追加新条目，不要重排已有插件，除非用户要求。

### 6. 校验

至少运行：

```bash
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
python3 -m json.tool plugins/<plugin-name>/.codex-plugin/plugin.json >/dev/null
git diff --check
```

同时校验图标：

- `interface.logo` 和 `interface.composerIcon` 都存在。
- 路径以 `./assets/` 开头，且文件真实存在。
- SVG 图标必须能被 XML parser 解析；PNG/JPG 图标至少确认文件存在且不是 0 字节。

同时校验每个导入 skill 的 frontmatter：

- 文件以 `---` 开头。
- 存在结束 `---`。
- frontmatter 包含非空 `name` 和 `description`。
- `name` 与 skill 目录名一致，除非上游已有明确命名理由；不一致时在最终说明。
- 不包含占位字段。

如果本机有可用的 `skill-creator` 或项目专用校验脚本，也运行它，但不要用它替代上述最小校验。

### 7. 提交和发布

提交前检查：

```bash
git status --short
git diff --stat
```

提交信息使用：

```text
Add <plugin-name> plugin
```

然后：

```bash
git push
codex plugin marketplace upgrade <marketplace_name>
```

升级后确认输出或本地远程缓存中能看到 `<plugin-name>`。如果 `upgrade` 失败，保留已 push 的 commit，并把失败命令、错误摘要和下一步写清楚。

## 最终回复

最终回复必须包含：

- `commit hash`
- `plugin name`
- 自动判断出的 `Category` 与能力型插件名；如果用户手动指定目标插件，也说明是用户指定
- `导入 skills 数量`
- `跳过 Deprecated 数量`
- `验证命令和结果`
- 图标是否已写入 `logo` / `composerIcon`
- Codex App 里应选择的远程 marketplace 入口：通常是 `tianzecn/ctz-codex-plugins` 或 marketplace 名 `ctz-codex-plugins`
- 未完成项或残余风险；没有就说明无明显残余风险
