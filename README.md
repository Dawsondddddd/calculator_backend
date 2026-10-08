# 计算器系统 - 后端

前后端分离计算器系统的后端服务。负责表达式校验、解析、计算，以及计算历史的数据库存储。

## 技术栈

- Python 3.8+（开发环境 3.13）
- Flask：提供 HTTP 接口
- 标准库 `sqlite3`：持久化计算历史
- 手写递归下降解析器：完成表达式解析，不使用 `eval` / `exec`

## 目录结构

```
backend/
├── app.py             # 路由层：接口定义、参数校验、返回 JSON
├── calculator.py      # 业务层：表达式解析与计算
├── database.py        # 数据层：SQLite 增删查
├── requirements.txt   # 依赖清单
├── README.md
└── codestyle.md
```

## 运行环境

- Windows / macOS / Linux
- Python 3.8 及以上
- pip

## 安装方法

```bash
cd backend
pip install -r requirements.txt
```

## 启动方法

```bash
cd backend
python app.py
```

启动成功后会打印监听地址，其中包含：

```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
```

本机访问用 <http://127.0.0.1:8000> 即可。

> `127.0.0.1` 是本机回环地址，只在本机启动服务后可访问，不要把这个地址当作公网地址分享给别人。

## 公网访问（Cloudflare Tunnel）

要让别人也能打开前端并真正完成计算，后端需要有一个公网地址。这里用 Cloudflare Tunnel 的 quick tunnel，不需要账号和信用卡：

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

启动后终端会打印一个 `https://xxxx.trycloudflare.com` 地址，把它填到前端的 `API_BASE` 即可。当前公开 Demo 使用：

<https://humanitarian-consecutive-makes-deeper.trycloudflare.com>

> quick tunnel 没有可用性保证，只在 `cloudflared` 进程运行期间有效，重启后会分配新地址。

### 长期稳定部署

需要 7x24 在线的地址时，可任选一种：

- 云平台部署 Flask 应用（如 PythonAnywhere、Railway、Fly.io），得到固定域名；
- Cloudflare 账号 + named tunnel，绑定自己的域名；
- 自备服务器跑 `gunicorn app:app`，前面再加 Nginx。

如果前端页面提示「无法连接后端服务」，按顺序检查：

1. 运行 `app.py` 的终端窗口没有关闭，输出中有 `Running on http://127.0.0.1:8000`；
2. 浏览器直接打开 <http://127.0.0.1:8000/api/health>，正常应返回 `{"success": true, "message": "ok"}`；
3. 前端 `index.html` 里的 `API_BASE` 与后端实际地址、端口一致。

## 配置说明

所有配置都在 `app.py` 顶部，并且都可以用环境变量覆盖（云平台部署时会自动注入 `PORT`）：

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `HOST` | `0.0.0.0` | 监听地址，`0.0.0.0` 表示本机和局域网都能访问 |
| `PORT` | `8000` | 监听端口 |
| `FLASK_DEBUG` | 空 | 设为 `1` 时开启调试模式 |

数据库文件和表达式长度限制分别在 `database.py`、`calculator.py` 中：

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `DB_PATH` | `backend/calculator.db` | SQLite 数据库文件 |
| `MAX_EXPRESSION_LENGTH` | `200` | 表达式最大长度 |

## 数据库初始化

服务启动时自动执行 `CREATE TABLE IF NOT EXISTS`，无需手动初始化。

表结构：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | INTEGER | 主键，自增 |
| `expression` | TEXT | 用户输入的表达式 |
| `result` | TEXT | 后端计算出的结果 |
| `created_at` | TEXT | 计算时间，格式 `YYYY-MM-DD HH:MM:SS` |

删除 `calculator.db` 文件即可清空数据并重新建库。

## API 接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/calculate` | 计算表达式并保存历史 |
| GET | `/api/history` | 查询全部历史记录 |
| DELETE | `/api/history/{id}` | 删除指定历史记录 |
| DELETE | `/api/history` | 清空历史记录（附加功能） |
| GET | `/api/health` | 健康检查 |

### 计算

请求：

```json
{ "expression": "(1+2)*3" }
```

成功响应（200）：

```json
{ "success": true, "id": 1, "expression": "(1+2)*3", "result": 9, "created_at": "2026-10-05 10:20:00" }
```

失败响应（400）：

```json
{ "success": false, "message": "除数不能为 0" }
```

### 查询历史

响应（200）：

```json
{ "success": true, "data": [ { "id": 1, "expression": "1+2", "result": "3", "created_at": "2026-10-05 10:20:00" } ] }
```

## 支持的表达式

- 四则运算：`+`、`-`、`*`、`/`
- 复合表达式与优先级：`1 + 2 * 3`
- 括号：`(1 + 2) * 3`
- 一元正负号：`-5 + 8`、`3 * -2`
- 小数：`1.5 * 2`

## 安全说明

表达式的解析和计算由 `calculator.py` 中手写的递归下降解析器完成，全程没有使用 `eval`、`exec` 或任何等价的可执行任意代码的方式。SQL 全部使用参数化查询。

## 前后端连接方式

后端默认监听 `http://127.0.0.1:8000`，并通过 `after_request` 对所有响应添加 CORS 头（`Access-Control-Allow-Origin: *`），前端可以跨端口或直接用 `file://` 打开时访问。

## 部署到 Render

仓库里已经带好 `render.yaml`，可以直接用 Render 的 Blueprint 流程部署到公网：

1. 打开 <https://dashboard.render.com/blueprints>，选择用 GitHub 账号登录并授权；
2. 点 `New Blueprint Instance`，选中本仓库 `calculator_backend`，分支选 `main`；
3. Render 会自动读取 `render.yaml`：免费套餐、`pip install -r requirements.txt` 构建、`gunicorn app:app` 启动、健康检查路径 `/api/health`；
4. 点 `Apply`，等待构建和部署完成，会得到一个形如 `https://calculator-backend-xxxx.onrender.com` 的公网地址。

验证方式：浏览器打开 `https://<你的地址>/api/health`，返回 `{"success": true, "message": "ok"}` 就说明后端已经在公网运行。

两点需要知道：

- 免费实例在一段时间没有请求后会休眠，下一次访问要等几十秒冷启动；
- 免费实例的磁盘是临时的，`calculator.db` 会随着重新部署或实例重启而重置，历史记录会清空。需要长期保存数据要挂载持久化磁盘或改用外部数据库。
