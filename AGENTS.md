# AGENTS.md

本仓库是 `ctz-codex-plugins`，用于把多个上游 skill 仓库打包成 Codex App 可安装的插件 marketplace。

## 通用协作规则

- 始终用简体中文回复。
- 编码前先说明假设；如果需求有多种解释，先点明差异，必要时询问。
- 优先用最少代码解决问题，不添加未被要求的功能、抽象或配置项。
- 只改和任务直接相关的文件；不要顺手重构、格式化或清理无关代码。
- 如果发现无关问题，可以在回复里说明，不要擅自删除或修复。
- 不要覆盖用户已有改动。开始修改前先查看 `git status --short --branch`。

## 仓库结构

- marketplace 入口：`.agents/plugins/marketplace.json`
- 插件目录：`plugins/<plugin-name>/`
- 插件清单：`plugins/<plugin-name>/.codex-plugin/plugin.json`
- skill 内容：`plugins/<plugin-name>/skills/`
- 项目说明：`README.md`

新增插件时，最小结构应保持为：

```text
plugins/<plugin-name>/
  .codex-plugin/plugin.json
  skills/
```

并在 `.agents/plugins/marketplace.json` 的 `plugins` 数组中添加对应条目。

## 修改原则

- 保留上游 skill 的真实内容和元数据，除非有明确原因需要做 Codex 兼容性调整。
- marketplace 条目的 `name` 应与插件目录名、`.codex-plugin/plugin.json` 里的 `name` 保持一致。
- `source.path` 使用相对路径，例如 `./plugins/<plugin-name>`。
- 默认分类沿用现有模式：`Productivity`。
- 不要把已废弃或未声明要发布的上游 skill 入口暴露为独立 skill。
- README 只在插件清单、安装方式或用户可见能力发生变化时更新。

## 验证清单

根据改动范围选择最小但足够的验证：

```bash
jq empty .agents/plugins/marketplace.json
find plugins -path '*/.codex-plugin/plugin.json' -exec jq empty {} +
git diff --check
```

如果改动包含 Python 脚本，额外运行：

```bash
python3 -m py_compile <script.py>
```

如果改动包含 TypeScript/JavaScript 脚本，优先使用该脚本目录已有的 `package.json` 命令；不要为了验证临时引入新工具链。

## 发布与本机可见性

- 刷新本机 marketplace 缓存可用：

```bash
codex plugin marketplace upgrade ctz-codex-plugins
```

- 缓存刷新成功不等于当前 Codex 会话会热更新插件/skill 列表。
- 如果用户反馈 App 里看不到插件，继续核对 `~/.codex/config.toml` 中是否存在并启用了：

```toml
[plugins."<plugin-name>@ctz-codex-plugins"]
enabled = true
```

- 涉及交付时，完成定义不只看仓库 diff；还要按用户要求核对 GitHub、Codex App 或 PromptHub 的真实可见、可安装、可启用状态。
