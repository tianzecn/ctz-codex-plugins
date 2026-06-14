<div align="center">

# huashu-weread

> *「不是查数据。是 AI 把你忘掉的那些时刻还给你。」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent-Agnostic](https://img.shields.io/badge/Agent-Agnostic-blueviolet)](https://skills.sh)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

**微信读书高阶顾问 · 在官方 weread skill 之上加一层「读书顾问的工作流」**

<br>

微信读书前几天上了一个官方 AI skill（[weread.qq.com/r/weread-skills](https://weread.qq.com/r/weread-skills)），把书架、笔记、阅读统计、推荐 6 件事开放给 AI。能力很强，但它只是「自然语言包装的搜索接口」——你让它推荐书，它不会去看你已经读过什么，常把你笔记 68 条的书又当新书推回来给你。

本 skill 在官方 8 个 API 之上，加一层「**读书顾问的工作流**」。核心方法是「**书架 + 笔记交叉分析**」——书架揭示你「主动归类的兴趣」，笔记揭示你「真读过的书」。只看书架会漏信号，只看笔记会错过兴趣方向。

```
npx skills add alchaincyf/huashu-weread
```

跨 agent 通用——Claude Code、Cursor、Codex、OpenClaw、Hermes 都能装。

[看效果对比](#看效果对比) · [装上就能用](#装上就能用) · [4 个 workflow](#4-个-workflow) · [核心方法](#核心方法书架--笔记交叉)

</div>

---

## 看效果对比

同样一个问题：「**推荐下产品经理方向的书**」。

**裸 weread skill 答：14 本通识书单**

按入门到进阶分了 6 个梯队，推《俞军产品方法论》《幕后产品》《硅谷增长黑客实战笔记》……都是好书，但：

- 《俞军产品方法论》我做了 **68 条笔记**
- 《幕后产品》**在我书架上躺着两年**
- 《硅谷增长黑客》我做了 **34 条笔记**

它根本没看我的笔记和书架，只是一个用自然语言包装的搜索接口。把读过的书又当新书推回来。

**huashu-weread 答：5 本针对你的拼图建议**

| 推荐 | 理由（基于你的实际阅读数据） |
|---|---|
| 《转型启示录》Marty Cagan | 你读了俞军、苏杰这一脉中国 PM 经典，但完全没碰 Cagan |
| 《设计心理学》诺曼 | 你方法论书一堆但 UX 根基缺 |
| 《AI Product Manager's Handbook》 | 你在做 AI 产品但 AI PM 书架空白 |
| 《重来》Jason Fried | 你是独立开发者但读的 PM 书大多是大公司视角 |
| 《重来 3》 | 你之前加了《小而美》没读完，这本是同一谱系更系统 |

最后还给「如果只读一本：X」和「如果想真正再上一个台阶：Y+Z」两个明确建议。

差距：**裸 weread 给的是「合格的通识书单」，huashu-weread 给的是「针对你这个人的拼图建议」**。

---

## 装上就能用

**前置依赖**：必须先装官方 weread skill（[weread.qq.com/r/weread-skills](https://weread.qq.com/r/weread-skills)），按页面指引走两步配置（复制安装指令 + 登录拿 API Key），全程不超过 1 分钟。

装完官方后，再装本 skill：

```bash
npx skills add alchaincyf/huashu-weread
```

跑起来：

```
"推荐下一本读啥"               → 自动走 advisor
"想系统搞懂行为经济学"          → 自动走 path
"整理下我在《掌控习惯》里的笔记"  → 自动走 alchemy
"写一篇我今年的读书复盘"        → 自动走 review
"我现在在读哪本"               → 轻量直答，一句话给进度
```

模糊的需求也认：「不知道读啥」「有相关的书吗」「这本书我记住了啥」「我今年读了什么」都能正确路由。

---

## 4 个 workflow

| Workflow | 干什么 | 触发话术 |
|---|---|---|
| **advisor** | 推荐下一本读什么。扒书架+笔记交叉，找拼图缺口，验证微信读书是否上架 | 「推荐书」「下一本读啥」「不知道读啥」 |
| **path** | 想搞懂一个领域。先判断你段位，再给入门→进阶→前沿的阶梯书单 | 「想搞懂 X」「从零入门 X」「系统学习 X」 |
| **alchemy** | 整理你的笔记。把零散划线想法提炼成有结构的读书笔记 | 「整理我的笔记」「这本书我记住了啥」 |
| **review** | 写读书复盘。给一段时间，输出能发朋友圈/公众号/小红书的复盘文章 | 「我今年读了什么」「年度盘点」 |

每个 workflow 都有独立的方法论文档，详见 [`workflows/`](workflows/)：

- [`workflows/advisor.md`](workflows/advisor.md) — 读书顾问标准流程
- [`workflows/path.md`](workflows/path.md) — 入门到前沿的阶梯规划
- [`workflows/alchemy.md`](workflows/alchemy.md) — 笔记提炼标准流程
- [`workflows/review.md`](workflows/review.md) — 读书复盘文章生成

---

## 核心方法：书架 + 笔记交叉

整套 skill 的方法论建立在三个数据源 × 三种交叉信号上。

### 三个数据源

| 源 | 接口 | 揭示什么 |
|---|---|---|
| 书架分类 | `/shelf/sync` 的 `archive[]` | 用户**主动给书归类**的兴趣方向 |
| 书架书目 | `/shelf/sync` 的 `books[]` | 加入书架的所有书 + 每本最近翻页时间 |
| 笔记列表 | `/user/notebooks` | 真做了笔记的书 + 每本笔记条数 |

### 三种交叉信号

**信号 1：真读 vs 放着**

| 状态 | 判定条件 | 含义 |
|---|---|---|
| 真读了 | 书架有 + notebooks 有 + 笔记 ≥ 5 | 吃进去了的书 |
| 放着没动 | 书架有 + notebooks 无 | 收藏癖，不是真兴趣 |
| 隐藏深读 | 书架无 + notebooks 有 + 笔记 ≥ 10 | 借/试读但真读了，常被推荐忽略 |
| 浅尝即止 | 书架有 + notebooks 笔记 1-3 条 | 翻了几页就放下 |

**信号 2：深度 vs 广度**——按笔记条数分层（≥20 重度，10-20 中度，3-10 轻度，1-3 翻过）

**信号 3：最近 vs 历史**——用 `readUpdateTime` 看最近 30 天活跃书目（用户当前兴趣常和书架分类不一致）

完整方法论见 [`shared/knowledge-map.md`](shared/knowledge-map.md)。

---

## vs 官方 weread skill

| 维度 | 官方 weread | huashu-weread |
|---|---|---|
| 定位 | 能力提供者（8 个 API） | 读书顾问（4 个 workflow） |
| 推荐书 | 调 `/store/search`，返回通识书单 | 先扒书架+笔记，再找拼图缺口 |
| 整理笔记 | 调 `/book/bookmarklist`，给原始数据 | 按主题聚类，提炼结构化笔记 |
| 阅读复盘 | 调 `/readdata/detail`，给统计数据 | 按平台（朋友圈/公众号/小红书）生成文章 |
| 是否会去看用户已读什么 | 否 | 是（书架+笔记交叉） |

不是替代关系——huashu-weread 在官方 8 个 API 之上加了一层 prompt 工程层。装上后官方 skill 还在底层跑，两个不冲突。

---

## 异常与边界

> 实操中常遇到的问题，全部有 fallback，绝不静默失败。详见 [`SKILL.md`](SKILL.md) 的「异常与边界条件」段。

- `WEREAD_API_KEY` 未设置 → 报错并告知怎么获取
- API 返回 `errcode != 0` → 重试 1 次，仍失败告知用户
- 出现 `upgrade_info` → 暂停操作，按指引升级版本
- notebooks 完全空（新用户）→ 退化到仅用书架推断，但明确告知准度会差
- 书架完全空 → 不走 advisor，建议先读几本或切 path workflow
- 用户主题模糊（如「想读点 AI 相关」）→ 在检查点先确认细分方向

所有数据展示遵守强制规范：Unix 时间戳转 `YYYY-MM-DD`，阅读时长秒转「X 小时 Y 分钟」，bookId 永远附 `weread://` 深度链接，绝不裸数字。

---

## 给 skill 开发者：本仓库的设计原则

如果你想做类似的「在原子 API 之上加一层工作流」的 skill，可以参考几个点：

1. **检查点设计**：在「分叉影响输出本质」的地方插入用户确认 gate，但日常小决策 AI 自己定，不打扰用户
2. **方法论先行**：所有 workflow 共享同一套核心方法论（书架+笔记交叉），workflow 只是不同场景的应用
3. **数据展示规范强制化**：时间戳、单位、深度链接的展示规则写进 SKILL.md 强制约束
4. **异常的 fallback 全部明示**：每种异常都有处理动作，不留「静默失败」的空间

---

## License

MIT — 个人 + 商业用途均可，无需授权。

---

## 致谢

- 微信读书官方 skill 把最难的事做完了（把账号数据通过 API 暴露给 AI）：[weread.qq.com/r/weread-skills](https://weread.qq.com/r/weread-skills)
- 灵感来源：花叔的 [女娲 .skill](https://github.com/alchaincyf/nuwa-skill)（把人物方法论蒸馏成 skill）。这次只是把蒸馏对象从「人」换成了「我自己的微信读书账号」。

---

<div align="center">

Made by [@AlchainHust](https://x.com/AlchainHust) · 公众号「花叔」

</div>
