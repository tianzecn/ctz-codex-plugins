---
name: wechat-article-exporter
description: 使用 wechat-article-exporter 导出微信公众号文章、调用开放 API、或部署本地/Docker 服务时使用。
---

# WeChat Article Exporter

用于处理微信公众号文章导出任务。上游项目是 `wechat-article/wechat-article-exporter`，不是 Codex skill 仓库；本 skill 封装它的实际使用路径，而不是复制整套 Nuxt 应用源码。

## 适用场景

- 用户给出微信公众号文章 URL，要求导出为 Markdown、HTML、Text 或 JSON。
- 用户要批量下载某个公众号、合集或文章列表。
- 用户要本机启动、Docker 私有化部署或检查 wechat-article-exporter 的接口。
- 用户要导出阅读量、评论、评论回复等数据，并愿意按上游文档获取 credentials。

## 快速判断

1. 单篇文章 URL：优先调用公共下载接口，最小化操作。
2. 批量下载、搜索公众号、合集下载：优先使用在线站点或本地 Web UI，因为这些流程依赖扫码登录和页面状态。
3. 阅读量、评论等私域数据：先提醒需要 credentials；没有 credentials 时不要假装能直接获取。
4. 私有化部署：优先 Docker；需要改源码或调试时才用本地 Node/Yarn。

## 单篇导出

公共站点：

```bash
curl -L --get "https://down.mptext.top/api/public/v1/download" \
  --data-urlencode "url=<微信公众号文章URL>" \
  --data-urlencode "format=markdown"
```

支持的 `format`：

- `html`
- `markdown`
- `text`
- `json`

保存文件时按格式选择扩展名，例如 `.md`、`.html`、`.txt`、`.json`。如果接口返回 `url不合法`，先确认 URL 是 `mp.weixin.qq.com` 的文章页，而不是公众号主页、搜一搜页或短链跳转页。

## 批量导出

优先使用在线站点：

- 下载站：`https://down.mptext.top`
- 文档站：`https://docs.mptext.top`

常见输出包括 HTML、JSON、Excel、TXT、Markdown、DOCX。HTML 更适合保留原文排版；Markdown 更适合后续总结、归档和知识库处理；Excel 更适合文章列表、阅读量、评论等结构化数据。

批量导出通常需要扫码登录公众号后台能力。用户没有登录或 credentials 时，只能完成公开单篇文章导出，不能承诺拿到完整公众号历史列表、阅读量或评论数据。

## 本地运行

源码运行要求 Node.js `>=22` 和 Yarn `1.22.22`：

```bash
git clone https://github.com/wechat-article/wechat-article-exporter
cd wechat-article-exporter
corepack enable
corepack prepare yarn@1.22.22 --activate
yarn install --frozen-lockfile
yarn dev
```

默认 Nuxt dev 服务通常监听 `http://localhost:3000`。启动后用浏览器访问本地地址，再按页面流程登录、搜索和导出。

## Docker 部署

上游 Dockerfile 暴露 `3000` 端口，并使用文件 KV：

```bash
docker build -t wechat-article-exporter .
docker run --rm -p 3000:3000 \
  -e NITRO_KV_DRIVER=fs \
  -e NITRO_KV_BASE=.data/kv \
  wechat-article-exporter
```

如果部署在服务器上，先确认安全边界：不要把带登录态、credentials 或内部代理能力的实例无保护地公开到公网。

## API 边界

- `/api/public/v1/download`：单篇公开文章导出，不需要 token。
- `/api/public/v1/account`：搜索公众号，依赖有效登录 token。
- `/api/public/v1/article`：获取文章列表，依赖有效登录 token 和 `fakeid`。

当用户请求 API 调用代码时，优先给最小可执行 `curl` 示例，再根据需要转换成 Python/Node。不要绕过上游登录要求。

## 验证

完成任务前至少做一项可验证检查：

- 单篇导出：确认目标文件非空，并抽查标题或正文片段。
- 本地/容器服务：确认端口可访问，例如 `curl -I http://localhost:3000` 或打开页面。
- API 调用：确认 HTTP 状态码和返回内容格式符合目标格式。
- 批量导出：确认导出文件数量、格式和样例内容，而不是只说任务已开始。
